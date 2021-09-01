# Tk windows

CHOOSE_EXCEL_WINDOW = "Elegir excel de datos"
CHOOSE_IMAGE_WINDOW = "Elegir imagen"
CHOOSE_MULTIPLE_IMAGES_WINDOW = "Elegir imagenes"
CHOOSE_DIRECTORY_WINDOW = "Elegir carpeta"
CHOOSE_VIDEO_WINDOW = "Elegir video para calcular métricas"
CHOOSE_MULTIPLE_VIDEOS_WINDOW = "Elegir videos para calcular métricas"
WRITE_FILENAME = "Escriba el nombre del archivo"

# Windows titles
PROCESS_LIST_WIDGET_TITLE = "Lista de procesamiento"
PROCESS_LIST_TITLE = "Procesos realizados:"

GLOBAL_ROUTINE_PARAMS_WIDGET_TITLE = "Parámetros de rutina global"


# Extensions

TIF_EXTENSION = ".tif"

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

MOVEMENT_VIEW_TITLE = "Mapa de calor del movimiento"
TEXTURE_IMAGE_VIEW_TITLE = "Mapa de calor de la textura de la imagen"
TEXTURE_VIDEO_VIEW_TITLE = "Mapa de calor de la textura del video"

# Error messages

ERROR_TITLE = "Error ocurrido"

UNKNOWN_ERROR = "Ha ocurrido un error inesperado. La interfaz volverá a un estado seguro para evitar errores de " \
                "arrastre "
UNKNOWN_ERROR_TYPE = "Tipo de error: "

NO_METRIC_SELECTED = "Debe seleccionar almenos una metrica"
NO_IMAGE_FILE = "El archivo seleccionado no es una imagen. \n\nSolo se admiten las siguientes extensiones: \n.tif"
NO_EXCEL_FILE = "El archivo seleccionado no es un excel. Debe tener la extensión '.xlsx'"
NO_EXCEL_FILES = "Alguno de los archivos seleccionados no es un excel. Deben tener la extensión '.xlsx'"
NO_VIDEO_FILE = "El archivo seleccionado no es un video. Debe tener la extensión '.avi'"
NO_VIDEO_FILES = "Alguno de los archivos seleccionados no es un video. Deben tener la extensión '.avi'"
NO_PATH_SELECTION = "No se seleccionó ningun path"
NO_MGAC_METHOD_ERROR = "No se aplico el metodo mgac en la imagen aún"
NO_ALL_IMAGES_READY_FOR_ANALYZE_METRIC_DESCRIPTION = "Para la comparación de la métrica es necesario haber calculado " \
                                                     "el mapa de movimiento y el mapa de textura de imagen y video"
NO_PROFILE_SELECTED_ERROR = "No se seleccionó ningún perfil para analizar"
NO_LINE_SELECTED_ERROR = "La figura utilizada para este método debe ser una línea"
NO_IMAGE_LOADED = "No se cargó ninguna imagen para analizar. Debe elegir una imagen '.tif' en el menu 'Archivo'"
NO_PROCESS_USED = "Para añadir un proceso de umbralización adaptativa, mueva los spinners hasta que la imagen " \
                  "quede con el formato deseado"

BOTH_SAVE_OPTIONS_SELECTED_EXCEPTION = "No pueden estar ambas opciones seleccionadas"
NO_SAVE_OPTIONS_SELECTED_EXCEPTION = "No se seleccionó ninguna opción de guardado"

VIEW_NOT_FOUND = "Vista no encontrada"

# Wait message

WAIT_SAVING_FILES_TITLE = "Guardando archivos"
WAIT_SAVING_FILES_DESC = "Los archivos generados se están guardando. Esta acción puede tomar unos minutos..."

WAIT_ESTIMATION_MESSAGE_TITLE = "Estimación"
WAIT_ESTIMATION_MESSAGE_DESC = "Se esta estimando el costo de tiempo y espacio de la rutina. Espere unos segundos... "

WAIT_TEXTURE_IMAGE_MESSAGE_TITLE = "Textura de imagen"
WAIT_TEXTURE_IMAGE_MESSAGE_DESC = "Se esta generando el mapa de textura de la imagen. Espere unos segundos... "

# Confirmation messages

DEFAULT_PARAMETERS_MANUAL_ROUTINE_TITLE = "Restaurar defaults"
DEFAULT_PARAMETERS_MANUAL_ROUTINE_DESCRIPTION = "¿Esta seguro que quiere volver a tener los parámetros default en todas" \
                                                " las rutinas? Se sobreescribirán los actuales"

GLOBAL_ROUTINE_ESTIMATION_TITLE = "Estimación de resultados"
GLOBAL_ROUTINE_TIME_ESTIMATION = "Estimación de tiempo requerido: "
GLOBAL_ROUTINE_MEMORY_ESTIMATION = "Estimación de memoria requerida: "
GLOBAL_ROUTINE_MEMORY_ESTIMATION_2 = " (cota máxima)"

NO_REGION_FOUND_TITLE = "Confirmación de región"
NO_REGION_FOUND_DESCRIPTION = "No se seleccionó ninguna región. Se tomará como región toda la imagen"

# Information messages

INFORMATION_TITLE = "Information"

PROGRESS_BAR_CANCELLED = "Progreso cancelado"

ADAPTIVE_THRESHOLD_WINDOW_SIZE_HELP = "Tamaño de la vecindad de píxeles utilizada para calcular un valor de umbral para el " \
                                      "píxel central. Un tamaño de ventana de 5 representa un entorno de 5x5 alrededor del " \
                                      "píxel. \n\nEl valor puede ser tanto par como impar debido a que los valores pares se " \
                                      "transforman dentro del método al siguiente impar. \n" "Los valores recomendados son " \
                                      "entre 5 y 13. Valores muy chicos dejaran ruido en la imagen y valores muy grandes " \
                                      "delimitarán la célula de forma poco precisa."
ADAPTIVE_THRESHOLD_C_CONSTANT_HELP = "Es una constante que se resta al valor del umbral calculado mediante la ventana. " \
                                     "Valores muy altos harán que toda la imagen se umbralice a cero (fondo negro). " \
                                     "Los valores recomendados son entre 3 y 7. "
ADAPTIVE_THRESHOLD_METHOD_HELP = "Umbralización de la media: El valor final del umbral que se calcula es la media de los " \
                                 "píxeles de la ventana menos el valor C. " \
                                 "\nUmbralización gaussiana: El valor final del umbral que se calcula es la suma pesada " \
                                 "de los píxeles de la ventana menos el valor C."
ADAPTIVE_THRESHOLD_ALGORITHM_HELP = "Una vez que haya determinado el tamaño de ventana, la constante C y el método " \
                                    "para calcular el umbral haz click en 'Añadir proceso' para agregar este proceso a la " \
                                    "cola de procesos que se aplicarán en Generación de video --> Generar video de " \
                                    "célula con procesos. \n\nMediante las barras deslizantes se puede ver como cambia " \
                                    "la imagen en el panel de la izquierda."

ANISOTROPIC_FILTER_TIMES_HELP = "Número de veces que se aplica el filtro sobre la imagen. Los valores recomendados " \
                                "son entre 1 y 6 iteraciones. El valor óptimo depende de la cantidad de ruido que posee " \
                                "la imagen."
ANISOTROPIC_FILTER_ALGORITHM_HELP = "Una vez que haya cargado una imagen y determinado el número de iteraciones, haz click " \
                                    "en 'Aplicar' para eliminar el ruido de la imagen. Los resultados se verán reflejados en " \
                                    "el panel de la izquierda."

MGAC_ITERATIONS_HELP = "Es una de las condiciones de corte. El algoritmo puede terminar cuando la toda región inicial marcada " \
                       "ya haya llegado a un borde o debido a que se alcanza el número de iteraciones. " \
                       "En cada iteración cada píxel de la región inicial se contrae o expande."
MGAC_THRESHOLD_HELP = "Es el valor del umbral para poder considerar a un píxel frontera."
MGAC_SMOOTHING_HELP = "El smoothing representa que tan exacta va a ser la curva de la región con respecto al " \
                      "objeto. A mayor suavizado se obtiene una curva más redondeada, pero su exactitud es menor. "
MGAC_BALLOON_HELP = "El valor indica que si la región inicial marcada debe contraerse o expandise en cada iteración. Un valor " \
                    "de negativo indica que debe contraerse y un valor positivo indica que debe expandirse."
MGAC_ALPHA_HELP = "El parámetro es utilizado por el algoritmo del gradiente gaussiano. Este parámetro hace que los " \
                  "bordes encontrados en la imagen sean más oscuros a mayor valor. Los valores recomendados están entre " \
                  "100 y 300"
MGAC_SIGMA_HELP = "El parámetro es utilizado por el algoritmo del gradiente gaussiano. Este parámetro indica el tamaño " \
                  "de la ventana utilizada, a mayor valor de la ventana menos zonas serán tomadas como bordes. Los " \
                  "valores recomendados están entre 2 y 5"
MGAC_ALGORITHM_HELP = "Una vez que haya cargado una imagen, haya trazado la región inicial sobre la misma, " \
                      "haya determinado la cantidad de iteraciones, el valor del umbral, el smoothing, el valor de balloon " \
                      "y las opciones secundarias, haz click en 'Aplicar' para obtener el contorno de la célula. Se abrirá una " \
                      "ventana donde podrá ver la ejecución del algoritmo paso por paso."

TEXTURE_PROFILE_ALGORITHM_HELP = "Una vez que haya cargado una imagen, haya trazado una línea (vertical, horizontal " \
                                 "u diagonal) sobre la misma haz click en 'Aplicar' para obtener el resultado " \
                                 "de la textura a lo largo del perfil. Se abrirá una ventana donde podra ver los resultados."

TEXTURE_CLASSIFICATION_IMAGE_CLUSTERS_HELP = "Cantidad de grupos (clusters) en los que se clasificará a los valores de la " \
                                             "textura de la imagen. Al ser un mapa de calor, representa la cantidad de colores " \
                                             "del mismo."
TEXTURE_CLASSIFICATION_IMAGE_ALGORITHM_HELP = "Una vez cargada la imagen y determinada la cantidad de clústers, haz click " \
                                              "en 'Clasificar' para obtener el mapa de calor de la imagen. Se abrirá una " \
                                            "ventana que contiene el mapa de calor, aunque el mismo también se podrá ver en el " \
                                            "panel de la izquierda."
TEXTURE_CLASSIFICATION_VIDEO_THRESHOLD_HELP = "Valor que se utilizará para umbralizar la imagen y separar la célula del fondo. " \
                                            "Los valores recomendados son entre 12 y 25, dependiendo la intensidad de la imagen."
TEXTURE_CLASSIFICATION_VIDEO_CLUSTERS_HELP = "Cantidad de grupos en los cuales se clasificará a los valores de la textura de " \
                                             "cada imagen del video. Al ser un mapa de calor, representa la cantidad de " \
                                             "colores del mismo. "
TEXTURE_CLASSIFICATION_VIDEO_ALGORITHM_HELP = "Una vez cargada la imagen y determinado el valor del umbral y la cantidad de " \
                                              "clústers, haz click en 'Clasificar' para obtener el mapa de calor del video. " \
                                              "Se abrirá una ventana que contiene el mapa de calor, aunque el mismo " \
                                              "también se podrá ver en el panel de la izquierda."

GENERATE_MOVEMENT_HEAT_MAP_THRESHOLD_HELP = "Valor que se utilizará para umbralizar la imagen y separar la célula del fondo. " \
                                            "Los valores recomendados son entre 12 y 25, dependiendo la intensidad de la imagen."
GENERATE_MOVEMENT_HEAT_MAP_ALGORITHM_HELP = "Una vez cargada la imagen y determinado el valor de umbral, haz click en " \
                                            "'Generar mapa de calor' para obtener el mapa de calor de la imagen. Se abrirá una " \
                                            "ventana que contiene el mapa de calor, aunque el mismo también se podrá ver en el " \
                                            "panel de la izquierda."

ANALYZE_MOVEMENT_AND_TEXTURE_GENERATE_VIEWS_HELP = "Una vez cargada la imagen y determinado los parámetros para cada vista, " \
                                                   "haz click en 'Generar vistas'. Espere hasta que se terminen de generar los " \
                                                   "mapas de calor y proceda haciendo click en 'Analizar'."
ANALYZE_MOVEMENT_AND_TEXTURE_ALGORITHM_HELP = "Una vez que haya generado las vistas, haz click en 'Analizar' para poder " \
                                              "obtener los mapas comparativos. Puede seleccionar una región cuadrada sobre " \
                                              "la cual calcular los resultados. Se abrirá una ventana donde podrá ver " \
                                              "los resultados."

GENERATE_METRICS_LOAD_HELP = "Cargue la ruta al archivo que contiene la máscara de la imagen."
GENERATE_METRICS_ALGORITHM_HELP = "Una vez cargada la ruta del archivo que contiene a la máscara y seleccionada las " \
                                  "métricas a calcular, haz click en 'Generar métricas' para generar un excel donde se " \
                                  "guardan las métricas calculadas de la célula. Este excel se guardará dentro de la " \
                                  "carpeta Métricas, que se encuentra en la ruta asignada como carpeta de Output en la " \
                                  "solapa Archivo"

GENERATE_MULTIPLE_CELLS_METRICS_ALGORITHM_HELP = "Una vez cargada la ruta del archivo que contiene a la máscara y " \
                                                 "seleccionada la/s métrica/s a calcular, haz click en 'Generar métricas' " \
                                                 "para generar un excel por célula donde se " \
                                                 "guardan las métricas calculadas de la célula. " \
                                                 "Estos excel se guardará dentro de la " \
                                                 "carpeta Métricas, que se encuentra en la ruta asignada como " \
                                                 "carpeta de Output en la " \
                                                 "solapa Archivo"

PLOT_METRICS_LOAD_HELP = "Cargue la ruta al archivo .xlsx que contiene la información para generar los gráficos."
PLOT_METRICS_ALGORITHM_HELP = "Una vez cargada la ruta al archivo .xlsx y elegidas la/s métrica/s para graficar, haz click " \
                              "en 'Graficar métricas'. Se abrirán tantas ventanas como métricas se grafiquen."

PLOT_METRICS_DISTRIBUTION_ALGORITHM_HELP = "Elija la/s métrica/s para graficar su distribución y haz click en 'Graficar " \
                                           "distribución'. Deberá seleccionar el archivo .xlsx del cuál se tomará la " \
                                           "información. Se abrirán tantas ventanas como métricas se grafiquen."

VIDEO_GENERATOR_ALGORITHM_HELP = "Una vez que se haya cargado una imagen y se hayan agregado los métodos en la cola " \
                                 "haz click en 'Iniciar' para aplicar dicha secuencia de métodos en cada frame " \
                                 "del video de la imagen seleccionada."

GLOBAL_ROUTINE_ALGORITHM_HELP = "Una vez determinado que subrutinas se ejecutarán y la forma de guardado de los resultados " \
                                "haz click en 'Iniciar' para seleccionar la carpeta que contiene las células a las que se le " \
                                "quiere aplicar la rutina global. Se puede seleccionar una carpeta con una o más células. " \
                                "\n\nAparecerá un ventana con el tiempo que llevará procesar la rutina completa, para seguir " \
                                "haz click en 'Continuar', de lo contrario en 'Cancelar'. " \
                                "Los resultados estarán guardados dentro de la carpeta Generado."

# Progress Bar

CANCEL_BUTTON_TEXT = "Cancelar"
CONTINUE_BUTTON_TEXT = "Continuar"

CALCULATE_PERIMETERS_TITLE = "Calculo de perímetro"
CALCULATE_PERIMETERS_DESCRIPTION = "Calculando perímetros"

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

# Simple Metrics plot

PERIMETER_PLOT_TITLE = "Perímetro en el tiempo"
PERIMETER_X_LABEL = "Perímetro en píxeles"

AREA_PLOT_TITLE = "Área en el tiempo"
AREA_X_LABEL = "Área en píxeles"

AXIS_RATIO_PLOT_TITLE = "Razón de ejes en el tiempo"
AXIS_RATIO_X_LABEL = "Razón de ejes"

SIMPLE_METRICS_Y_LABEL = "Tiempo en frames"

# Distribution Metrics plot

PERIMETER_DISTRIBUTION_TITLE = "Distribucion de perímetros"
PERIMETER_DISTRIBUTION_X_LABEL = "Valores de perímetro en pixeles"

AREA_DISTRIBUTION_TITLE = "Distribución de áreas"
AREA_DISTRIBUTION_X_LABEL = "Valores de areas en pixeles"

AXIS_RATIO_DISTRIBUTION_TITLE = "Distribución de razon de ejes"
AXIS_RATIO_DISTRIBUTION_X_LABEL = "Valores de razón de ejes"

DISTRIBUTION_METRICS_Y_LABEL = "Frecuencia"

# Titles of some global routine metric plots

GLOBAL_ROUTINE_SIMPLE_METRICS_PLOT_TITLE = "Área, perímetro y razón de ejes en el tiempo"
GLOBAL_ROUTINE_DISTRIBUTION_METRICS_PLOT_TITLE = "Distribución de área, perímetro y razón de ejes"

# Comparison plot

ORIGINAL_VS_ACTUAL_TITLE = "Original vs Actual"
ORIGINAL_TITLE = "Imagen Original"
ACTUAL_TITLE = "Imagen Actual"

MOVEMENT_VS_TEXTURE_IMAGE_TITLE = "Movimiento vs Textura-Imagen"
MOVEMENT_TITLE = "Imagen de Movimiento"
TEXTURE_IMAGE_TITLE = "Imagen de Textura-Imagen"

MOVEMENT_VS_TEXTURE_VIDEO_TITLE = "Movimiento vs Textura-Video"
TEXTURE_VIDEO_TITLE = "Imagen de Textura-Video"

TEXTURE_IMAGE_VS_TEXTURE_VIDEO = "Textura-Imagen vs Textura-Video"

FOUR_GRID_COMPARISON = "Valor de la región en las 4 vistas"

CBAR_MOVEMENT_LABEL = "Movimiento"
CBAR_TEXTURE_LABEL = "Textura"

