from preprocessing import *

def main():
  '''Driver function to demo preprocessing. Given a path to a directory of high 
  pass filtered images, will return the labels (i.e. distances to the focal plane)
  and file paths of clean image data with distances capped at distance_cap.'''

  # Set variable values to get some output with sample_data images
  FILE_PATH = "../sample_data/level1_jpeg/"
  extension = "jpeg"
  img_height = 1200
  img_width = 1920
  intensity_thresh = 0.50
  eap_thresh = 0.03 # Probably lower than what would be used in practice
  distance_cap = 20

  # Run through preprocessing steps (assuming we already have HP filtered images)
  labels, all_coords, img_paths = get_filename_data(FILE_PATH, ext="jpeg", quiet=False)
  clean_infocus_coords = get_clean_infocus_coords(all_coords, labels, img_paths, 
                                                  img_height, img_width, 
                                                  intensity_thresh=intensity_thresh, 
                                                  eap_thresh=eap_thresh)
  clean_labels, clean_paths = get_clean_data(clean_infocus_coords, all_coords, 
                                             labels, img_paths)
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
