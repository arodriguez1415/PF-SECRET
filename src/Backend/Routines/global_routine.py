from src.Backend.Video_processing_algorithms.multiple_cells_video_generator import generate_mask_video_of_all_cells


def routine():
    masked_videos_paths_list = generate_mask_video_of_all_cells()

    array_images_list = video_file_manipulation.get_video_as_array(mask_video_path)