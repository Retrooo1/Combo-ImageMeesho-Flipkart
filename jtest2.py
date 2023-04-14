import cv2
import numpy as np
import os

def run(margin,color,size, input_folder, output_folder):
    # input_folder = "receievedPath"
    # output_folder = "savedPath"

    if os.path.exists(output_folder) == False:
        os.mkdir(output_folder)

    files = os.listdir(input_folder)

    totalCount = len(files) ** 2
    cnt = 0

    for file1 in files:
        for file2 in files:
            cnt += 1
            if file1 != file2:
                img1 = cv2.imread(input_folder + '/' + file1)
                img2 = cv2.imread(input_folder + '/' + file2)

                h1, w1 = img1.shape[:2]
                h2, w2 = img2.shape[:2]

                resized = cv2.resize(img2, (w1, h1), interpolation=cv2.INTER_AREA)

                # margin = 25

                # vis = np.ones((h1 + (2 * margin), w1 + w1 + (3 * margin), 3), np.uint8) * 255  # 255=White, 0=Black
                vis = np.ones((h1 + (2 * margin), w1 + w1 + (3 * margin), 3), np.uint8) * color  # 255=White, 0=Black
                vis[margin:h1 + margin, margin:w1 + margin, :3] = img1
                vis[margin:h1 + margin, w1 + (2 * margin):w1 + w1 + (2 * margin), :3] = resized
                # vis = cv2.resize(vis,(3378,2552), interpolation = cv2.INTER_AREA)
                vis = cv2.resize(vis,size, interpolation = cv2.INTER_AREA)
                cv2.imwrite(output_folder + "/" + file1[:-4] + "&" + file2, vis)
                print("Made image #", cnt, " out of",totalCount)

