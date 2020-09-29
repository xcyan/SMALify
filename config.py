from os.path import join
import cv2
import time

# Define paths to each dataset
data_path = "data"
BADJA_PATH = "data/BADJA"
STANFORD_EXTRA_PATH = "data/StanfordExtra"
OUTPUT_DIR = "checkpoints/{0}".format(time.strftime("%Y%m%d-%H%M%S"))

CROP_SIZE = 256 
VIS_FREQUENCY = 100
GPU_IDS = "0" # GPU number to run on (not applicable for CPU)

# Run settings (I wouldn't recommend changing these unless you have good reason)
FORCE_SMAL_PRIOR = False # Allow the more recent Unity-based prior for dogs.
ALLOW_LIMB_SCALING = True # Allow scaling parameters, see Who Left the Dogs Out?

# Sequence/Image Settings
SHAPE_FAMILY = 1 # Choose from Cat (e.g. House Cat/Tiger/Lion), Canine (e.g. Dog/Wolf), Equine (e.g. Horse/Zebra), Bovine (e.g. Cow), Hippo
SEQUENCE_OR_IMAGE_NAME = "badja:rs_dog"
# SEQUENCE_OR_IMAGE_NAME = "stanfordextra:n02092339-Weimaraner/n02092339_748.jpg"
IMAGE_RANGE = range(0, 10) # Frames to process from sequence. Ignored for stanford extra
WINDOW_SIZE = 10 # Changed number of frames processed in one go.

# SMAL
SMAL_FILE = join(data_path, 'smal', 'my_smpl_00781_4_all.pkl')
SMAL_DATA_FILE = join(data_path, 'smal', 'my_smpl_data_00781_4_all.pkl')
SMAL_UV_FILE = join(data_path, 'smal', 'my_smpl_00781_4_all_template_w_tex_uv_001.pkl')
SMAL_SYM_FILE = join(data_path, 'smal', 'symIdx.pkl')

# PRIORS
WALKING_PRIOR_FILE = join(data_path, 'priors', 'walking_toy_symmetric_pose_prior_with_cov_35parts.pkl')
UNITY_SHAPE_PRIOR = join(data_path, 'priors', 'unity_betas.npz')

# DATALOADER
IMG_RES = 224

# RENDERER
MESH_COLOR = [0, 172, 223]

# OPTIMIZER - You may
OPT_WEIGHTS = [
    [25.0, 10.0, 7.5, 5.0], # Joint
    [0.0, 0.0, 100.0, 250.0], # Sil Reproj
    [0.0, 100.0, 50.0, 10.0], # Betas
    [0.0, 10.0, 5.0, 1.0], # Pose
    [0.0, 100.0, 100.0, 100.0], # Limits TODO!
    [0.0, 0.1, 0.1, 0.1], # Splay
    [500.0, 100.0, 100.0, 100.0], # Temporal
    [300, 1000, 1000, 1000], # Num iterations
    [1e-2, 5e-3, 5e-3, 5e-3]] # Learning Rate


# JOINT DEFINITIONS
TORSO_JOINTS = [2, 5, 8, 11, 12, 23]

CANONICAL_MODEL_JOINTS = [
  10, 9, 8, # upper_left [paw, middle, top]
  20, 19, 18, # lower_left [paw, middle, top]
  14, 13, 12, # upper_right [paw, middle, top]
  24, 23, 22, # lower_right [paw, middle, top]
  25, 31, # tail [start, end]
  34, 33, # ear base [left, right]
  35, 36, # nose, chin
  38, 37, # ear tip [left, right]
  39, 40, # eyes [left, right]
  15, 15, # withers, throat (TODO: Labelled same as throat for now), throat 
  28] # tail middle

# indicate invalid joints (i.e. not labelled) by -1
BADJA_ANNOTATED_CLASSES = [
    14, 13, 12, # upper_left [paw, middle, top]
    24, 23, 22, # lower_left [paw, middle, top]
    10, 9, 8, # upper_right [paw, middle, top]
    20, 19, 18, # lower_right [paw, middle, top]
    25, 31, # tail [start, end] (note, missing the tail middle point)
    -1, -1, # ear base [left, right]
    33, -1, # nose, chin (note, missing the 'jaw base' point)
    36, 35, # ear tip [left, right]
    -1, -1, # eyes [left, right]
    -1, 15, # withers, throat
    28] # tail middle

# Visualization
MARKER_TYPE = [
    cv2.MARKER_TRIANGLE_DOWN, cv2.MARKER_STAR, cv2.MARKER_CROSS, # upper_left
    cv2.MARKER_TRIANGLE_DOWN, cv2.MARKER_STAR, cv2.MARKER_CROSS, # lower_left
    cv2.MARKER_TRIANGLE_DOWN, cv2.MARKER_STAR, cv2.MARKER_CROSS, # upper_right
    cv2.MARKER_TRIANGLE_DOWN, cv2.MARKER_STAR, cv2.MARKER_CROSS, # lower_right
    cv2.MARKER_CROSS, cv2.MARKER_TRIANGLE_DOWN, # tail
    cv2.MARKER_CROSS, cv2.MARKER_CROSS, # right_ear, left_ear
    cv2.MARKER_CROSS, cv2.MARKER_STAR, # nose, chin
    cv2.MARKER_TRIANGLE_DOWN, cv2.MARKER_TRIANGLE_DOWN, # right_tip, left_tip
    cv2.MARKER_CROSS, cv2.MARKER_CROSS, # right_eye, left_eye
    cv2.MARKER_CROSS, cv2.MARKER_CROSS, # withers, throat
    cv2.MARKER_STAR] # tail middle
    
MARKER_COLORS = [
    [230, 25, 75], [230, 25, 75], [230, 25, 75], # upper_left, red
    [255, 255, 25], [255, 255, 25], [255, 255, 25], # lower_left, yellow
    [60, 180, 75], [60, 180, 75], [60, 180, 75], # upper_right, green
    [0, 130, 200], [0, 130, 200], [0, 130, 200], # lower_right, blue
    [240, 50, 230], [240, 50, 230], # tail, majenta
    [255, 153, 204], [29, 98, 115], # left_ear, pink & right_ear, turquoise 
    [245, 130, 48], [245, 130, 48], # nose, chin
    [255, 153, 204], [29, 98, 115], # left_ear, pink & right_tip, turquoise
    [0, 0, 0], [0, 0, 0], # right eye, left eye: black
    [128, 0, 0], [128, 0, 0], # withers, throat, maroon
    [240, 50, 230]] # tail middle

N_POSE = 34 # not including global rotation
N_BETAS = 20 # number of SMAL shape parameters to optimize over