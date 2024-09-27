% Generate sample noisy data for demonstration
x = linspace(-10, 10, 100);    % x data
true_A = 1.0;                  % True amplitude
true_mu = 0.0;                 % True mean
true_sigma = 2.0;              % True standard deviation
true_C = 0.5;                  % True baseline (offset)

% Create noisy Gaussian data
y = true_A * exp(-(x - true_mu).^2 / (2 * true_sigma^2)) + true_C + 0.1*randn(size(x));

% Plot the noisy data
figure;
plot(x, y, 'bo');
title('Noisy Data');
xlabel('x');
ylabel('y');
hold on;

% Define the custom Gaussian model with an offset
gaussian_model = fittype('A*exp(-(x-mu)^2/(2*sigma^2)) + C', ...
                         'independent', 'x', ...
                         'coefficients', {'A', 'mu', 'sigma', 'C'});

% Initial guesses for the fit parameters (optional)
initial_guess = [1, 0, 2, 0.5];  % [A, mu, sigma, C]

% Fit the model to the noisy data
[fit_result, gof] = fit(x', y', gaussian_model, 'StartPoint', initial_guess);

% Plot the fitted curve
plot(fit_result, 'r-');  % Fitted Gaussian
legend('Noisy Data', 'Fitted Gaussian');
hold off;

% Display the fitted parameters
disp(fit_result);

% You can access individual parameters like:
A_fitted = fit_result.A;
mu_fitted = fit_result.mu;
sigma_fitted = fit_result.sigma;
C_fitted = fit_result.C;

% Optionally, print the fitted parameters
fprintf('Fitted parameters: A = %.4f, mu = %.4f, sigma = %.4f, C = %.4f\n', ...
        A_fitted, mu_fitted, sigma_fitted, C_fitted);
