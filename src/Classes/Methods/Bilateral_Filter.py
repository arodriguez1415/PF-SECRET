class Bilateral_Filter:

    def __init__(self, sigma_r, sigma_s, window_size):
        self.name = "Bilateral Filter"
        self.sigma_r = sigma_r
        self.sigma_s = sigma_s
        self.window_size = window_size
