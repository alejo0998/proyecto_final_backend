from re import I
from aprendizaje.models import Sena
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf

mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities
IMAGE_HEIGHT , IMAGE_WIDTH = 1280, 720 
SEQUENCE_LENGTH = 30        #ACÁ DECÍA 20, LE SUBÍ A 150 PORQUE LA MAYORÍA LOS FILMAMOS A 30 FPS Y DURAN COMO MUCHO 5 SEG
DATASET_DIR = '../media' 


class Video():

  def __init__(self):
    self.frames = []
    self.keypoints = []
    self.label = ""
    self.path = ""

def getKeypoints(self):
  return self.keypoints

def getLabel(self):
  return self.label
  

def mediapipe_detection(image, model):
    #image = cv2.resize(image, (IMAGE_HEIGHT, IMAGE_WIDTH))
    #image = image / 255
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)      # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                       # Image is no longer writeable
    results = model.process(image)                      # Make prediction
    image.flags.writeable = True                        # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

#def draw_landmarks(image, results):
#    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS) # Draw face connections
#    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS) # Draw pose connections
#    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
#    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw right hand connections

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else zero(33*4,"pose")
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else zero(468*3,"cara")
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else zero(21*3,"mano izq")
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else zero(21*3,"mano der")
    return np.concatenate([pose, face, lh, rh])

def zero(i,t):
  print("no encontro " + str(t))
  return np.zeros(i)


def frames_extraction(video_memory, categoria):
    print("Estoy extrayendo los frames")
    '''
    This function will extract the required frames from a video after resizing and normalizing them.
    Args:
        video_path: The path of the video in the disk, whose frames are to be extracted.
    Returns:
        frames_list: A list containing the resized and normalized frames of the video.
    '''

    # Declare a list to store video frames.
    #frames_list = []
    results = []
    video_keypoints = []
    video = Video()
    video.label = categoria
    
    # Read the Video File using the VideoCapture object.
    video_reader = cv2.VideoCapture(video_memory.file.name)

    # Get the total number of frames in the video.
    video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the the interval after which frames will be added to the list.
    skip_frames_window = max(int(video_frames_count/SEQUENCE_LENGTH), 1)

    # Iterate through the Video Frames.
    for frame_counter in range(SEQUENCE_LENGTH):

        # Set the current frame position of the video.
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

        # Reading the frame from the video. 
        success, frame = video_reader.read() 

        # Check if Video frame is not successfully read then break the loop
        if not success:
            break

        # Resize the Frame to fixed height and width.
        resized_frame = cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
        #resized_frame = cv2.cvtColor(resized_frame,cv2.COLOR_BGR2RGB)
        #cv2_imshow(frame)
        # Normalize the resized frame by dividing it with 255 so that each pixel value then lies between 0 and 1
        #normalized_frame = resized_frame / 255

        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
          # Make detections
          image, result = mediapipe_detection(resized_frame, holistic)
          
          # Draw landmarks
          #draw_landmarks(image, result)
          results = extract_keypoints(result)
          video_keypoints.append(results)
          """print("mano izq")
          print(result)
          if(result.left_hand_landmarks):
            print(len(result.left_hand_landmarks.landmark))"""
          # Show to screen
          #cv2_imshow(image)
        
        # Append the normalized frame into the frames list
        #frames_list.append(image)
        
    # Release the VideoCapture object. 
    video_reader.release()
    #video.frames = frames_list
    video.keypoints = video_keypoints

    
    # Return the frames list.
    return video
    #return frames_list, video_keypoints

def predict(video, categoria):
    categoria = categoria
    model_name = categoria
    file_name = './modelos/' + model_name + ".h5"
    model = tf.keras.models.load_model(file_name, compile = False)
    print("Cargue el modelo")
    video = frames_extraction(video, categoria)
    print("Extraje los frames")
    test_keypoints = list(video.keypoints)
    list_test = list()
    list_test.append(test_keypoints)
    predictions = model.predict((np.array(list_test)))
    print("Ya predije")
    posibles_senas = Sena.objects.filter(categoria=categoria)[0:4]
    if len(posibles_senas) != len(predictions[0]):
      return None
    return posibles_senas[int(np.argmax(predictions))]
