from masking import *

def get_folder_with_num_name(num, parent_folder):
  """
  Finds the folder with the given numerical name in the specified parent folder.

  Args:
    num: The desired numerical value of the folder name.
    parent_folder: The path to the parent folder containing the numbered folders.

  Returns:
    The full path to the folder with the given numerical name, or None if not found.
  """

  for folder_name in os.listdir(parent_folder):
    try:
      folder_num = int(folder_name)
      # print(folder_num)
      if folder_num == num:
        return os.path.join(parent_folder, folder_name)
    except ValueError:
      # Ignore non-numeric folder names
      pass
  return None

def make_masked_strokes(normal_paths, mask_paths, save_location):
# Initialize drawing number
    # Given a folder like Profile
    # We want to iterate through files like 18_0c81e49b-5163-4d03-b294-45ffea5e50a2.jpg
    # And get the drawing number, 18
    current_draw_num = -1
    for mask_img in os.listdir(mask_paths):
        # While the drawing number doesn't change
        draw_num = int(os.path.basename(mask_img).split("_")[0])
        if current_draw_num != int(draw_num):
            # Given a folder like dataset1
            # We want to get the NAME = int version of each folder name 00000018 ----> 18
            # And get the normal.jpg in that folder
            current_draw_num = draw_num
            normal_map_folder = get_folder_with_num_name(current_draw_num, normal_paths)
            normal_map_img = normal_map_folder + "\\" + "normal.jpg"
            # print(normal_map_img)
            # print(mask_paths + "\\" + mask_img)
    # Then we want to call create_masked_img on the
        create_masked_img(normal_map_img, mask_paths + "\\" + mask_img, save_location)

normal_paths = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset1"
mask_paths = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified\\Profile"
save_location = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified_masked\\Profile"
make_masked_strokes(normal_paths, mask_paths, save_location)
print("Done1!")

normal_paths = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset1"
mask_paths = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified\\Contour"
save_location = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified_masked\\Contour"
make_masked_strokes(normal_paths, mask_paths, save_location)
print("Done2!")

normal_paths = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset1"
mask_paths = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified\\Detail"
save_location = "C:\\Users\\andre\\Documents\\github\\auto-lineweights\\datasets\\dataset5\\simplified_masked\\Detail"
make_masked_strokes(normal_paths, mask_paths, save_location)
print("Done3!")