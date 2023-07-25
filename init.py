from os import getenv
from dotenv import load_dotenv
from google.cloud import storage
import gcsfs
import pickle

load_dotenv()

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
PROJECT_ID = getenv("PROJECT_ID")
CREDENTIAL_FILE = getenv("CREDENTIAL_FILE")
OUTPUT_BUCKET = getenv("OUTPUT_BUCKET")

def get_credentials():
    fs = gcsfs.GCSFileSystem(project=PROJECT_ID)
    with fs.open(CREDENTIAL_FILE, "rb") as handle:
        cred = pickle.load(handle)
    return cred

credentials = get_credentials()

gcs_client = storage.Client(PROJECT_ID)
gcp_bucket_output = gcs_client.get_bucket(OUTPUT_BUCKET)

snippet_features = ["title","publishedAt","channelId","channelTitle","categoryId","description"]

unsafe_characters = ['\n', '\r', '"']

category_dict = {0: 'All', 1: 'Film & Animation', 2: 'Autos & Vehicles',
                 10: 'Music', 15: 'Pets & Animals', 17: 'Sports',
                 19: 'Travel & Events', 20: 'Gaming', 22: 'People & Blogs',
                 23: 'Comedy', 24: 'Entertainment', 25: 'News & Politics',
                 26: 'Howto & Style', 27: 'Education', 28: 'Science & Technology',
                 42: 'Shorts'}