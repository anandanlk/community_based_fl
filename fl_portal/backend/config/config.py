from pymongo import MongoClient
import os

# MongoDB Atlas
# uri = "mongodb+srv:"
# atlas_collection = MongoClient(uri)['communityFL']['users']
# db = atlas_collection

# Local MongoDB
local_collection = MongoClient('mongodb://localhost:27017/')['communityFL']['users']
db = local_collection

communication_server_ip = "16.171.3.132"

# path_to_workflow="/Users/anand/DecentralizedFL/CWL_Workflow"
# Ensure both CommunityFL and Decentralized FL projects are pulled to same parent directory
current_directory = os.path.dirname(os.path.abspath(__file__))
relative_path_to_target = '../../../DecentralizedFL/CWL_Workflow'
path_to_workflow = os.path.abspath(os.path.join(current_directory, relative_path_to_target))
