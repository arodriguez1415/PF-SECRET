# Plot figures save paths for load

MGAC_BORDER_IMAGE_SAVE_NAME = "border_image.tiff"
MGAC_MASK_IMAGE_SAVE_NAME = "mask_image.tiff"
COMPARISON_CELL_VS_MASK_SAVE_NAME = "cell_vs_mask.tiff"
ANISOTROPIC_IMAGE_SAVE_NAME = "anisotropic_image.tiff"

# view names

MAIN_VIEW = "Main View"
MOVEMENT_VIEW = "Movement"
TEXTURE_IMAGE_VIEW = "Texture Image"
TEXTURE_VIDEO_VIEW = "Texture video"

# Error messages

NO_PATH_SELECTION = "No se seleccionó ningun path"
NO_MGAC_METHOD_ERROR = "No se aplico el metodo mgac en la imagen aún"
NO_ALL_IMAGES_READY_FOR_ANALYZE_METRIC_DESCRIPTION = "Para la comparación de la métrica es necesario haber calculado " \
                                                     "el mapa de movimiento y el mapa de textura de imagen y video"
NO_PROFILE_SELECTED_ERROR = "No se selecciono ningún perfil para analizar"
NO_LINE_SELECTED_ERROR = "La figura utilizada para este método debe ser una línea"

# Wait message

WAIT_ESTIMATION_MESSAGE_TITLE = "Estimacion"
WAIT_ESTIMATION_MESSAGE_DESC = "Se esta estimando el costo de tiempo y espacio de la rutina. Espere unos segundos... "

WAIT_TEXTURE_IMAGE_MESSAGE_TITLE = "Textura de imagen"
WAIT_TEXTURE_IMAGE_MESSAGE_DESC = "Se esta generando el mapa de textura de la imagen. Espere unos segundos... "

# Confirmation messages

GLOBAL_ROUTINE_ESTIMATION_TITLE = "Estimación de resultados"
GLOBAL_ROUTINE_TIME_ESTIMATION = "Estimación de tiempo requerido: "
GLOBAL_ROUTINE_MEMORY_ESTIMATION = "Estimación de memoria requerida: "
GLOBAL_ROUTINE_MEMORY_ESTIMATION_2 = " (cota máxima)"

NO_REGION_FOUND_TITLE = "Confirmación de región"
NO_REGION_FOUND_DESCRIPTION = "No se seleccionó ninguna región. Se tomará como región toda la imagen"

# Information messages

INFORMATION_TITLE = "Information"

ADAPTIVE_THRESHOLD_WINDOW_SIZE_HELP = "Mensaje de prueba para mostrar una informacion"
ADAPTIVE_THRESHOLD_C_CONSTANT_HELP = "Mensaje de prueba para mostrar una informacion"
ADAPTIVE_THRESHOLD_METHOD_HELP = "Mensaje de prueba para mostrar una informacion"
ADAPTIVE_THRESHOLD_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

ANISOTROPIC_FILTER_TIMES_HELP = "Mensaje de prueba para mostrar una informacion"
ANISOTROPIC_FILTER_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

MGAC_ITERATIONS_HELP = "Mensaje de prueba para mostrar una informacion"
MGAC_THRESHOLD_HELP = "Mensaje de prueba para mostrar una informacion"
MGAC_SMOOTHING_HELP = "Mensaje de prueba para mostrar una informacion"
MGAC_BALLOON_HELP = "Mensaje de prueba para mostrar una informacion"
MGAC_ALPHA_HELP = "Mensaje de prueba para mostrar una informacion"
MGAC_SIGMA_HELP = "Mensaje de prueba para mostrar una informacion"
MGAC_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

TEXTURE_PROFILE_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

TEXTURE_CLASSIFICATION_IMAGE_CLUSTERS_HELP = "Mensaje de prueba para mostrar una informacion"
TEXTURE_CLASSIFICATION_IMAGE_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"
TEXTURE_CLASSIFICATION_VIDEO_THRESHOLD_HELP = "Mensaje de prueba para mostrar una informacion"
TEXTURE_CLASSIFICATION_VIDEO_CLUSTERS_HELP = "Mensaje de prueba para mostrar una informacion"
TEXTURE_CLASSIFICATION_VIDEO_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

GENERATE_MOVEMENT_HEAT_MAP_THRESHOLD_HELP = "Mensaje de prueba para mostrar una informacion"
GENERATE_MOVEMENT_HEAT_MAP_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

ANALYZE_MOVEMENT_AND_TEXTURE_GENERATE_VIEWS_HELP = "Mensaje de prueba para mostrar una informacion"
ANALYZE_MOVEMENT_AND_TEXTURE_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

GENERATE_METRICS_LOAD_HELP = "Mensaje de prueba para mostrar una informacion"
GENERATE_METRICS_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

GENERATE_MULTIPLE_CELLS_METRICS_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

PLOT_METRICS_LOAD_HELP = "Mensaje de prueba para mostrar una informacion"
PLOT_METRICS_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

PLOT_METRICS_DISTRIBUTION_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

GLOBAL_ROUTINE_ALGORITHM_HELP = "Mensaje de prueba para mostrar una informacion"

# Progress Bar

CANCEL_BUTTON_TEXT = "Cancelar"
CONTINUE_BUTTON_TEXT = "Continuar"

CALCULATE_PERIMETERS_TITLE = "Calculo de perimetro"
CALCULATE_PERIMETERS_DESCRIPTION = "Calculando perimetros"

CALCULATE_AREA_TITLE = "Calculo de área"
CALCULATE_AREA_DESCRIPTION = "Calculando área"

CALCULATE_AXIS_RATIO_TITLE = "Calculo de razón de ejes"
CALCULATE_AXIS_RATIO_DESCRIPTION = "Calculando razón de ejes"

CALCULATE_METRICS_TITLE = "Calculo de métricas"
CALCULATE_METRICS_DESCRIPTION = "Calculando métricas"

GENERATE_VIDEO_TITLE = "Generación video de célula"
GENERATE_VIDEO_DESCRIPTION = "Generando frames"

GENERATE_MOTION_HEAT_MAP_TITLE = "Mapa de calor de movimiento"
GENERATE_MOTION_HEAT_MAP_DESCRIPTION = "Generando mapa de calor de movimiento"

GENERATE_TEXTURE_HEAT_MAP_TITLE = "Mapa de calor de textura"
GENERATE_TEXTURE_HEAT_MAP_DESCRIPTION = "Generando mapa de calor de textura"

GLOBAL_ROUTINE_PROGRESS_BAR_TITLE = "Rutina Global"

# Metrics plot

PERIMETER_PLOT_TITLE = "Perímetro en el tiempo"
PERIMETER_X_LABEL = "Perímetro en píxeles"
PERIMETER_Y_LABEL = "Tiempo en frames"

AREA_PLOT_TITLE = "Área en el tiempo"
AREA_X_LABEL = "Área en píxeles"
AREA_Y_LABEL = "Tiempo en frames"

AXIS_RATIO_PLOT_TITLE = "Razón de ejes en el tiempo"
AXIS_RATIO_X_LABEL = "Razón de ejes"
AXIS_RATIO_Y_LABEL = "Tiempo en frames"

# Comparison plot

ORIGINAL_VS_ACTUAL_TITLE = "Original vs Actual"
ORIGINAL_TITLE = "Imagen Original"
ACTUAL_TITLE = "Imagen Actual"

MOVEMENT_VS_TEXTURE_IMAGE_TITLE = "Movimiento vs Textura-Imagen"
MOVEMENT_TITLE = "Imagen de Movimiento"
TEXTURE_IMAGE_TITLE = "Imagen de Textura-Image"

MOVEMENT_VS_TEXTURE_VIDEO_TITLE = "Movimiento vs Textura-Video"
TEXTURE_VIDEO_TITLE = "Imagen de Textura-Video"

TEXTURE_IMAGE_VS_TEXTURE_VIDEO = "Textura-Imagen vs Textura-Video"

FOUR_GRID_COMPARISON = "Valor de la región en las 4 vistas"

# Windows titles
PROCESS_LIST_WIDGET_TITLE = "Lista de procesamiento"
GLOBAL_ROUTINE_PARAMS_WIDGET_TITLE = "Parámetros de rutina global"
