from preprocessing import *

def main():
  '''Driver function to demo preprocessing. Given a path to a directory of 
  source microscopy images, will perform edge detection via a high pass filter
  and return the labels (i.e. distances to the focal plane) and file paths of 
  clean image data with distances capped at distance_cap.'''

  # Set variable values to get some output with sample_data images
  #FILE_PATH = "../sample_data/level1_jpeg/"
  SRC_PATH = "../sample_data/level1/"
  HPF_PATH = "../sample_data/demo_hpf_jpegs/"
  src_ext = "tiff"
  hpf_ext = "jpeg"
  hpf_kernel_size = 13
  img_height = 1200
  img_width = 1920
  intensity_thresh = 0.50
  # This edge area percentage threshold is lower than what we might use in
  # practice, but it should let the demo find "clean" images in sample_data.
  eap_thresh = 0.05
  distance_cap = 20

  # Run through preprocessing steps
  src_img_paths = get_img_paths(SRC_PATH, src_ext)
  print("Performing edge detection with high pass filter...")
  filter_imgs(src_img_paths, hpf_kernel_size, HPF_PATH, hpf_ext)
  print("Parsing distances to the focal plane and image coordinates from filenames...")
  labels, all_coords, img_paths = get_filename_data(HPF_PATH, ext=hpf_ext, quiet=False)
  print("Finding clean images...")
  clean_infocus_coords = get_clean_infocus_coords(all_coords, labels, img_paths, 
                                                  img_height, img_width, 
                                                  intensity_thresh=intensity_thresh, 
                                                  eap_thresh=eap_thresh)
  clean_labels, clean_paths = get_clean_data(clean_infocus_coords, all_coords, 
                                             labels, img_paths)
  print("Applying cap to clean images...")
  capped_labels, capped_paths = get_capped_data(clean_labels, clean_paths, 
                                                cap=distance_cap)
  # Print out example filenames of clean images below cap
  show_found = min(5, len(capped_paths))
  print("Images above edge area percentage threshold and below focal distance cap:",len(capped_paths))
  print("Found:")
  for i in range(show_found):
    print(capped_paths[i])
  print("And {} others.".format(len(capped_paths) - show_found))
  return

if __name__ == "__main__":
  main()
