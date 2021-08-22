import cv2 as cv

# Feature types for saving

CONTOUR_VIDEO = "Video de máscara de célula"
SIMPLE_CELL_VIDEO = "Video de célula"
COMPARISON_VIDEO = "Video comparativo entre célula y máscara"
SIMPLE_METRICS_GRAPHS = "Gráficos de métricas simples"
DISTRIBUTION_METRICS_GRAPHS = "Gráficos de distribución de métricas"
METRICS_EXCEL = "Métricas en excel"
MOVEMENT_IMAGE = "Mapa de calor de movimiento"
TEXTURE_IMAGE = "Mapa de calor de textura"
MOVEMENT_AND_TEXTURE_COMPARISON_IMAGE = "Comparación de textura y movimiento"


# --- Normalize options ---

FROM_0_TO_255 = 255
FROM_0_TO_1 = 1

# MGAC attributes

MGAC_NAME = "MGAC"
MGAC_ITERATIONS = "Iteraciones"
MGAC_THRESHOLD = "Umbral"
MGAC_SMOOTHING = "Suavizado"
MGAC_BALLOON = "Fuerza de contracción o expansión"
MGAC_ALPHA = "Alpha"
MGAC_SIGMA = "Sigma"

# Adaptive threshold attributes

ADAPTIVE_THRESHOLD_NAME = "Umbralización adaptativa"
ADAPTIVE_THRESHOLD_WINDOW_SIZE = "Tamaño de ventana de vecinos"
ADAPTIVE_THRESHOLD_C_CONSTANT = "Constante C"
ADAPTIVE_THRESHOLD_METHOD = "Método"

# Anisotropic filter attributes

ANISOTROPIC_TIMES = "Iteraciones del filtro anisotrópico"
ANISOTROPIC_FILTER_NAME = "Filtro anisotrópico"

# Original method attributes

ORIGINAL_NAME = "Imagen original"

# --- Line Texture Profile

HORIZONTAL_LINE_TYPE = "Horizontal"
VERTICAL_LINE_TYPE = "Vertical"
DIAGONAL_LINE_TYPE = "Diagonal"

# --- Adaptative threshold mathods ---

ADAPTIVE_THRESHOLD_MEAN = cv.ADAPTIVE_THRESH_MEAN_C
ADAPTIVE_THRESHOLD_GAUSSIAN = cv.ADAPTIVE_THRESH_GAUSSIAN_C

ADAPTIVE_THRESHOLD_MEAN_NAME = "Umbralización de la media"
ADAPTIVE_THRESHOLD_GAUSSIAN_NAME = "Umbralización gaussiana"

# --- Metrics save method ---

# Metrics names
PERIMETER_METRIC = "Perimeter"
AREA_METRIC = "Area"
AXIS_RATE_METRIC = "Axis Rate"

BORDER_FRACTAL_DIMENSION_METRIC = "Borde - Dimension Fractal"
PERINUCLEAR_FRACTAL_DIMENSION_METRIC = "Perinúcleo - Dimension Fractal"
NUCLEAR_FRACTAL_DIMENSION_METRIC = "Núcleo - Dimension Fractal"

BORDER_MOVEMENT_METRIC = "Borde - Movimiento"
PERINUCLEAR_MOVEMENT_METRIC = "Perinúcleo - Movimiento"
NUCLEAR_MOVEMENT_METRIC = "Núcleo - Movimiento"


# Metrics dataframe headers
PERIMETER_HEADER = "Perimeter"
AREA_HEADER = "Area"
AXIS_RATE_HEADER = "Axis Rate"

BORDER_FRACTAL_DIMENSION_HEADER = "Borde - Dimension Fractal"
PERINUCLEAR_FRACTAL_DIMENSION_HEADER = "Perinúcleo - Dimension Fractal"
NUCLEAR_FRACTAL_DIMENSION_HEADER = "Núcleo - Dimension Fractal"

BORDER_MOVEMENT_HEADER = "Borde - Movimiento"
PERINUCLEAR_MOVEMENT_HEADER = "Perinúcleo - Movimiento"
NUCLEAR_MOVEMENT_HEADER = "Núcleo - Movimiento"

FRAMES_HEADER = "Frames"

# --- Texture classification---

# Methods

MEAN_SHIFT = "Mean shift"
K_MEANS = "K means"
KOHONEN = "Kohonen"
HDBSCAN = "HDBScan"

# Descriptors

GLCM_MEAN = "Mean"
GLCM_ENTROPY = "Entropy"
GLCM_HOMOGENEITY = "Homogeneity"
GLCM_DISSIMILARITY = "Dissimilarity"
LOCAL_ENTROPY = "Local_Entropy"
SHANNON_ENTROPY = "Shannon"


# Global routine -- Sub Routines

CONTOUR_SUBROUTINE = "Contour sub routine"
COMPARISON_SUBROUTINE = "Comparison sub routine"
METRICS_SUBROUTINE = "Metrics sub routine"
MOVEMENT_SUBROUTINE = "Movement sub routine"
TEXTURE_SUBROUTINE = "Texture sub routine"

# Global routine -- Save forms

CELL_SAVE_FORM = "Por célula"
FEATURE_SAVE_FORM = "Por rutina"
