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

PERIMETER_METRIC = "Perimeter"
AREA_METRIC = "Area"
AXIS_RATE_METRIC = "Axis Rate"
BORDER_FRACTAL_DIMENSION_METRIC = "Border Fractal dimension"
PERINUCLEAR_FRACTAL_DIMENSION_METRIC = "Perinuclear Fractal dimension"
NUCLEAR_FRACTAL_DIMENSION_METRIC = "Nuclear Fractal dimension"

PERIMETER_HEADER = "Perimeter"
AREA_HEADER = "Area"
AXIS_RATE_HEADER = "Axis Rate"
BORDER_FRACTAL_DIMENSION_HEADER = "Border Fractal dimension"
PERINUCLEAR_FRACTAL_DIMENSION_HEADER = "Perinuclear Fractal dimension"
NUCLEAR_FRACTAL_DIMENSION_HEADER = "Nuclear Fractal dimension"
FRAMES_HEADER = "Frames"
