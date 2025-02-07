import cv2,os,time

def scanDir(viddir_path):
    '''Scans the directory where videos will be stored for only mp4s'''
    vid_paths = []
    dir = os.listdir(viddir_path)
    for files in dir:
        if '.mp4' in files:
            vid_paths.append(viddir_path + '\\' + files)
            #print(files)
    return(vid_paths)

def clearImgs():
    '''Removes all frame images stored within a direectory'''
    path = '..\Senior Design\VidtoImg\Images\\'
    files = os.listdir(path)
    for images in files:
        try:
            ###WARNING BE CAREFUL HERE AS COULD POTENTIALLY DELETE WRONG FILES MAKE SURE FILE PATH IS CORRECT
            if os.path.isfile(path+images):
                if 'frame' in images:
                    os.remove(path+images)
        except Exception as e:
            print('Failed Deletion %s. Reason %s' % ((path+images),e))

def VidBreakdown(output,vidfiles):
    ###SECOND WARNING THIS FUNCTION CALLS A FILE DELETION DOUBLE CHECK ALL PATHS FIRST
    clearImgs()

    for videos in vidfiles:
        frame_skip = 10 #RATE at which number of frames will be skipped 
        current_frame = cv2.VideoCapture(videos) #Object to break the videos into frames
        
        if not current_frame.isOpened():
            print("Error Opening Video")
        
        frame_count = 0 #Counter for number of frames captured per video
        while True:
            ret,frame = current_frame.read() #Reads the current frame and saves the image to frame
            if not ret:
                print("Video %s Ended" % (videos))
                break
            
            #Declaring where the image will be placed and the filename
            output_file = os.path.join(output, f"frame_{frame_count:04d}.jpg")
            frame_count +=1
            
            #writing the file into a directory
            cv2.imwrite(output_file,frame)
            
            current_frame.set(cv2.CAP_PROP_POS_FRAMES,frame_skip) #Sets the next read frame to frame skip CAP_PROP_POS_FRAMES determines that
            frame_skip +=10

    current_frame.release()
    cv2.destroyAllWindows()









if __name__ == '__main__':
    VidBreakdown('..\Senior Design\VidtoImg\Images',scanDir('..\Senior Design\VidtoImg\Videos'))


