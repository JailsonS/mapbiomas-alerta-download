import os
import numpy as np
import argparse
from PIL import Image

def crop_center(pil_img, n_pixel_at_boundaries):
    
    img_width, img_height = pil_img.size

    crop_width = img_width - 2
    crop_height = img_height - n_pixel_at_boundaries


    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def main(input_img, output_img):
    out_dir = os.path.abspath(output_img)

    im = Image.open(os.path.abspath(input_img))

    im_cropped = crop_center(im, 100)
    im2 = im_cropped.crop(im_cropped.getbbox())
    im2.save(out_dir)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--input_img', type=str,help="input image dir")
    parser.add_argument('--output_img', type=str, help="output image dir")
    args = parser.parse_args()

    main(input_img=args.input_img, output_img=args.output_img)