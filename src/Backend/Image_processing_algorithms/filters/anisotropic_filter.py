
def anisotropic_medical_filter_function(image):
    filter_image = anisotropic_diffusion_filter_medpy(image)
    # special_save_and_load_preprocessing_image(filter_image)
    # anisotropic_medical_filter_method = AnisotropicMedicalFilter()
    interface.preprocessing_methods.append(anisotropic_medical_filter_method)