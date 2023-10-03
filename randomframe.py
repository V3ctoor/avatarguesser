import os
import cv2
import random
import json
from moviepy.editor import VideoFileClip

# Directory containing your subdirectories with .mkv files
video_directory = '.'
# Directory to save the .jpg files
output_directory = 'randomframes'
# Output text file
output_text_file = 'video_to_frame.json'
# Counter for image filenames
image_counter = 0

def random_frame(video_path):
    clip = VideoFileClip(video_path)
    # Avoid first or last 10% of the video
    min_time = clip.duration * 0.1
    max_time = clip.duration * 0.9
    frames = []
    for _ in range(100):
        random_time = random.uniform(min_time, max_time)
        frame = clip.get_frame(random_time)
        frames.append(frame)
    return frames

def save_frame(frame, output_path):
    # Convert the frame from RGB to BGR (OpenCV uses BGR instead of RGB)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # Reduce the size to 1/4
    new_size = (frame.shape[1] // 2, frame.shape[0] // 2)
    frame = cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)
    # Save the frame as a .jpg file
    cv2.imwrite(output_path, frame)

def main():
    global image_counter
    # Create output directory if it does not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Dictionary to store video to frame mapping
    video_to_frame_dict = {}

    # Go through all subdirectories in the current directory
    for subdir in os.listdir(video_directory):
        subdir_path = os.path.join(video_directory, subdir)
        if os.path.isdir(subdir_path):
            # Go through all .mkv files in this subdirectory
            for filename in os.listdir(subdir_path):
                if filename.endswith('.mkv'):
                    video_path = os.path.join(subdir_path, filename)

                    # Parse the episode name from the filename
                    episode_name = filename.split('.')[4:-2]
                    episode_name = ' '.join(episode_name)

                    frames = random_frame(video_path)
                    frame_filenames = []
                    for frame in frames:
                        output_filename = str(image_counter) + '.jpg'
                        output_path = os.path.join(output_directory, output_filename)
                        save_frame(frame, output_path)
                        frame_filenames.append(output_filename)
                        image_counter += 1

                    # Add the mapping to the dictionary
                    video_to_frame_dict[episode_name] = frame_filenames

                    print(f'Saved frames for {episode_name} to {output_path}')

    # Write the dictionary to the text file
    with open(output_text_file, 'w') as f:
        json.dump(video_to_frame_dict, f, indent=4)

if __name__ == '__main__':
    main()