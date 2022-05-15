""" Generates an ASCII video rendering each frame in ASCII """
from ascii_pic import asciify
import cv2
import sys
import os
import ffmpeg

from render_alphabet import Alphabet, ALPHABET_DIR


def ascii_vid(video_path, output_dir, output_file, output_fps):
    """ Renders a video in ASCII """
    temp_filename = "temp.mp4"
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    print("Preparing...")
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dframe = int(fps // output_fps)
    output_frame_count = int(frame_count // dframe)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create new video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_dir + "/" + temp_filename, fourcc,
                            output_fps, (frame_width, frame_height))

    # Asciify frames
    print("Rendering video...")
    with Alphabet(ALPHABET_DIR) as alphabet:
        for (i, frame_no) in enumerate(range(0, frame_count, dframe)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            print("Rendering frame %d/%d..." % (i, output_frame_count))

            # Render frame
            success, frame = cap.read()
            if not success:
                break

            asciified = asciify(frame, alphabet)
            # for i in range(frame_no, frame_no + dframe):
            #     video.write(asciified)
            video.write(asciified)

    # Cleanup render
    cap.release()
    video.release()
    print("Render done.")

    # Copy audio
    print("Copying audio...")
    ascii_video = ffmpeg.input(output_dir + "/" + temp_filename)
    orig_video = ffmpeg.input(video_path)
    ffmpeg.output(orig_video.audio, ascii_video.video,
                  output_dir + "/" + output_file).run()

    # Cleanup audio
    os.remove(output_dir + "/" + temp_filename)
    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid command. The right format: ./ascii_vid.py [video_path]")
        exit(1)
    else:
        ascii_vid(sys.argv[1], "output", "output.mp4", 6)
