import cv2 as cv

# --- LBP methods ---

# original local binary pattern which is gray scale but not rotation invariant.
LBP_DEFAULT = "default"

# extension of default implementation which is gray scale and rotation invariant.
LBP_ROR = "ror"

# improved rotation invariance with uniform patterns and
# finer quantization of the angular space which is gray scale and rotation invariant.
LBP_UNIFORM = "uniform"

# non rotation-invariant uniform patterns variant which is only gray scale invariant
LBP_NRI_UNIFORM = "nri_uniform"

# --- Adaptative threshold mathods ---

ADAPTIVE_THRESHOLD_MEAN = cv.ADAPTIVE_THRESH_MEAN_C
ADAPTIVE_THRESHOLD_GAUSSIAN = cv.ADAPTIVE_THRESH_GAUSSIAN_C

# --- Metrics save method ---

# Metrics names
PERIMETER_METRIC = "Perimeter"
AREA_METRIC = "Area"
AXIS_RATE_METRIC = "Axis Rate"

BORDER_FRACTAL_DIMENSION_METRIC = "Border - Dimension Fractal"
PERINUCLEAR_FRACTAL_DIMENSION_METRIC = "Perinuclear - Dimension Fractal"
NUCLEAR_FRACTAL_DIMENSION_METRIC = "Nuclear - Dimension Fractal"

BORDER_MOVEMENT_METRIC = "Borde - Movimiento"
PERINUCLEAR_MOVEMENT_METRIC = "Perinuclear - Movimiento"
NUCLEAR_MOVEMENT_METRIC = "Nuclear - Movimiento"


# Metrics dataframe headers
PERIMETER_HEADER = "Perimeter"
AREA_HEADER = "Area"
AXIS_RATE_HEADER = "Axis Rate"

BORDER_FRACTAL_DIMENSION_HEADER = "Border - Dimension Fractal"
PERINUCLEAR_FRACTAL_DIMENSION_HEADER = "Perinuclear - Dimension Fractal"
NUCLEAR_FRACTAL_DIMENSION_HEADER = "Nuclear - Dimension Fractal"

BORDER_MOVEMENT_HEADER = "Borde - Movimiento"
PERINUCLEAR_MOVEMENT_HEADER = "Perinuclear - Movimiento"
NUCLEAR_MOVEMENT_HEADER = "Nuclear - Movimiento"

FRAMES_HEADER = "Frames"
