import numpy as np
import cv2
import time


def crop(image):
    y_nonzero, x_nonzero, _ = np.nonzero(image)
    if y_nonzero.shape[0] == 0 or x_nonzero.shape[0] == 0:
        return None
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]


image = cv2.imread("test_image.png")

cropped = crop(image)
h = cropped.shape[0]
w = cropped.shape[1]

image_top_len = len(cropped[0].nonzero()[0]) // cropped.ndim
image_bot_len = len(cropped[-1].nonzero()[0]) // cropped.ndim

c = (image_bot_len - image_top_len) // 2
print(image_top_len, image_bot_len, c)

src = np.array([[c, 0], [w-c, 0], [w, h], [0, h]], dtype=np.float32)
dst = np.array([[0, 0], [w, 0], [w, h], [0, h]], dtype=np.float32)
mat = cv2.getPerspectiveTransform(src, dst)

start = time.time()
# cropped = crop(image)
sheared = cv2.warpPerspective(cropped, mat, (w, h))

notes = 5
        
for i in range(notes):
    # The current chunk to process
    chunk = sheared[:, i * w // notes: (i + 1) * w // notes]
    cv2.imwrite(f"out{i}.png", chunk)

end = time.time()

cv2.imwrite("cropped.png", cropped)
cv2.imwrite("sheared.png", sheared)

print((end - start) * 1000)
