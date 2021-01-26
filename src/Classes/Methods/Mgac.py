class Mgac:

    def __init__(self, region, iterations, threshold, smoothing, balloon, alpha, sigma):
        self.name = "Mgac"
        self.iterations = iterations
        self.threshold = threshold
        self.smoothing = smoothing
        self.balloon = balloon
        self.alpha = alpha
        self.sigma = sigma
        self.region = region
