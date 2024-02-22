import cv2
from Utils import load_image
from Seam_Carving import seam_carving

if __name__ == "__main__":
    filepath = "./image/002.jpg"
    save_dir = "./image/carved/"

    is_color = False
    is_red_line = True
    is_preservation = False
    is_dom = True
    scale_factor = 0.5
    num_iterations = 140  # Number of iterations/seams to remove
    save_step = 1
    xxyy = (130, 435, 140, 415)

    image = load_image(filepath, is_color, scale_factor)
    result_image = seam_carving(filepath, save_dir, image, is_color, is_red_line, is_preservation, is_dom, num_iterations, save_step, *xxyy)

    # Display the original and result images
    cv2.imshow("Original Image", image)
    cv2.imshow("Result Image", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
