% Clear workspace and command window
clear; clc;

% Define the true parameters for the Gaussian with offset
true_A = 1.0;      % Amplitude
true_mu = 0.0;     % Mean (center of the peak)
true_sigma = 2.0;  % Standard deviation (width)
true_C = 0.5;      % Baseline offset

% Simulate denser sampling near the peak (e.g., around x = 0)
x_dense = linspace(-2, 2, 80);         % Dense data in the peak region
x_tails = [-10:0.5:-2, 2:0.5:10];     % Sparse data in the tails
x_combined = sort([x_dense, x_tails]); % Combine dense and sparse data

% Generate noisy Gaussian data with denser points near the peak
noise_level = 0.1; % Set the noise level
y_combined = true_A * exp(-(x_combined - true_mu).^2 / (2 * true_sigma^2)) + true_C + ...
             noise_level * randn(size(x_combined));

% Normalize the noisy data so the maximum value is 1
y_combined = y_combined / max(y_combined);

% Plot the normalized noisy data
figure
plot(x_combined, y_combined, 'bo');
title('Normalized Noisy Data with Denser Points Near the Peak');
xlabel('x');
ylabel('Normalized y');
hold on;

% Define the custom Gaussian model with an offset
gaussian_model = fittype('A*exp(-(x-mu)^2/(2*sigma^2)) + C', ...
                         'independent', 'x', ...
                         'coefficients', {'A', 'mu', 'sigma', 'C'});

% Set initial guesses for the fit parameters (optional, but recommended)
initial_guess = [1, 0, 2, 0.5];  % [A, mu, sigma, C]

% Fit the Gaussian model to the combined data
[fit_result, gof] = fit(x_combined', y_combined', gaussian_model, 'StartPoint', initial_guess);

% Plot the fitted Gaussian curve
plot(fit_result, 'r-');  % Red line for fitted Gaussian
legend('Normalized Noisy Data', 'Fitted Gaussian');
hold off;

% Display the goodness of fit and fitted parameters
disp('Fitted Parameters:');
disp(fit_result);

% Display goodness-of-fit statistics
disp('Goodness of Fit:');
disp(gof);

% Calculate FWHM (Full Width at Half Maximum)
sigma_fitted = fit_result.sigma;
FWHM = 2 * sqrt(2 * log(2)) * sigma_fitted;  % FWHM formula for Gaussian
fprintf('FWHM (Largeur à mi-hauteur): %.4f\n', FWHM);

% Calculate Contrast (Difference between the maximum y-value and baseline C)
% The peak of the Gaussian occurs at x = mu, so we calculate the peak value
x_peak = fit_result.mu;
y_peak = fit_result.A * exp(-(x_peak - fit_result.mu).^2 / (2 * fit_result.sigma^2)) + fit_result.C;

contrast = y_peak - fit_result.C;
fprintf('Contrast (Peak y-value - C): %.4f\n', contrast);

% Optionally, access other individual parameters like this:
A_fitted = fit_result.A;
mu_fitted = fit_result.mu;
C_fitted = fit_result.C;

% Print the fitted parameters
fprintf('Fitted parameters: A = %.4f, mu = %.4f, sigma = %.4f, C = %.4f\n', ...
        A_fitted, mu_fitted, sigma_fitted, C_fitted);
