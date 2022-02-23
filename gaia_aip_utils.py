import requests
import pyvo as vo
import os
from io import StringIO
import h5py
import s3fs
import corner
import pandas as pd

# run a single postgre sql query using API key
# usage: get_one_query("select * from gaiaedr3_contrib.source_id2split limit 10")
# it returns pandas dataframe
def get_one_query(qstr,verbose=False):
    name = 'GAIA@AIP'
    url = 'https://gaia.aip.de/tap'
    # You can also use your TAP API Token from the gaia.aip.de account: gaia.aip.de->RightUpperMenu->API token
    token = "" #"Token XXX"

    if verbose:
        print('\npyvo version %s \n' % vo.__version__)
        print('TAP service %s \n' % name)

    # Setup authorization
    tap_session = requests.Session()
    tap_session.headers['Authorization'] = token

    jobs = []
    # open the connection
    tap_service = vo.dal.TAPService(url, session=tap_session)
    job = tap_service.submit_job(qstr, language='postgresql', runid='pybatch',queue="2h")
    job.run()
    jobs.append(job)
    i=0
    dfvec=[]
    for job in jobs:
        if verbose: print('getting results:',i)

        if verbose: print('getting results from ' + str(job.job.runid))
        job.raise_if_error()

        job.wait(phases=["COMPLETED", "ERROR", "ABORTED"], timeout=10.)
        if verbose:print(str(job.job.runid) + ' ' + str(job.phase))

        if job.phase in ("ERROR", "ABORTED"):
            pass
        else:
            results = job.fetch_result()
            dfvec.append(results.to_table().to_pandas())
        i=i+1
    return pd.concat(dfvec)

# locate 1 split file by source_id
def source_id2split(source_id):
    split=""
    qstr = f'select * from gaiaedr3_contrib.source_id2split as s where s.source_id={source_id} limit 1'
    df=get_one_query(qstr)
    return int(df.split[0])

# Find all the OK sources in StarHorse from a (short-ish) list of source_ids and get the split file names:
def get_id2split_multiple_ids(idlist):
    qstr = f'select * from gaiaedr3_contrib.source_id2split as s where s.source_id={idlist[0]}'
    for id in idlist:
        qstr += f'or s.source_id={id}'
    df=get_one_query(qstr)
    return df

# Get a posterior PDF file (by split ID)
def get_splitfile(split_id):
    if 'x' in vars():
        try:
            fs.close()
            h5f.close()
        except:
            pass # Was already closed
    # connect to public Bucket
    fs= s3fs.S3FileSystem(anon=True,client_kwargs={'endpoint_url':"https://s3.data.aip.de:9000"})
    filename1="s3://sh21pdf/gaiaedr3_sh_input_healpixlevel5_hpno-"+split_id+".fits.hdf5.h5"
    h5file=fs.open(filename1)
    return h5py.File(h5file, 'r')
    
def pdf_plot_by_id(f, iid):
    ndim, nsamples = 5, 100000
    np.random.seed(42)
    iikeys = np.int64(list(h5f.keys()))
    ii = [i for i,x in enumerate(iikeys) if x == source_id][0]
    iid = list(f.keys())[ii]
    example  = f[iid]
    # extract GMM from HDF5 files
    data1 = np.random.multivariate_normal(np.array(example['Gauss1_means']), np.array(example['Gauss1_covs']), size=int(example["weights"][0]*nsamples))
    data2 = np.random.multivariate_normal(np.array(example['Gauss2_means']), np.array(example['Gauss2_covs']), size=int(example["weights"][1]*nsamples))
    data3 = np.random.multivariate_normal(np.array(example['Gauss3_means']), np.array(example['Gauss3_covs']), size=int(example["weights"][2]*nsamples))
    samples = np.vstack([data1, data2, data3])
    # corner plot
    plt.figure(figsize=(8,8))
    figure = corner.corner(samples, plot_datapoints=False, show_titles=True, smooth=True,
                           labels=[r"$M_{\rm act}\ [M_{\odot}]$", r"Age [Gyr]", r"[Z/H]", "$d$ [kpc]", r"$A_V$ [mag]"],
                           range=[0.995, 0.995, 0.995, 0.995, 0.995], use_math_text=True, 
                           label_kwargs={"fontsize":25}, title_kwargs={"fontsize":22})
    # Extract the axes
    axes = np.array(figure.axes).reshape((ndim, ndim))
    figure.subplots_adjust(right=1.5,top=1.5)
    for ax in figure.get_axes():
        ax.tick_params(axis='both', labelsize=16)
    ax = axes[1, 1]
    #plt.text(3., 1.5, r'source_id '+ str(iid), horizontalalignment='center',
    #         verticalalignment='center', transform = ax.transAxes)
    plt.savefig("im/corner-" + iid +"png", dpi=100, bbox_inches="tight")