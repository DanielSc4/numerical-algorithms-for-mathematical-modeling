compute_cholesky("ex15.mat");
disp('1')
compute_cholesky("shallow_water1.mat")
disp('2')
compute_cholesky("parabolic_fem.mat")
disp('3')
compute_cholesky("apache2.mat")
disp('4')
compute_cholesky("G3_circuit.mat")
disp('5')
compute_cholesky("cfd1.mat")
disp('6')
compute_cholesky("cfd2.mat")
disp('7')
compute_cholesky("Flan_1565.mat")
disp('8')
compute_cholesky("StocF-1465.mat")
disp('9')



function [relative_error] = compute_cholesky_relative_error(matrix_name)
    A = load("./matrix/" + matrix_name);
    A = A.Problem.A;
    xe = ones(size(A, 1), 1);
    b = A * xe;
    x = A \ b;
    relative_error = norm(x - xe, 1) / norm(xe, 1);
end


function [read_time, solve_time] = compute_cholesky_read_and_solve_time(matrix_name)
    read_time = tic;
    A = load("./matrix/" + matrix_name);
    read_time = toc(read_time);
    solve_time = tic;
    A = A.Problem.A;
    xe = ones(size(A, 1), 1);
    b = A * xe;
    x = A \ b;
    solve_time = toc(solve_time);
end


function [read_times, solve_times] = cholesky_times(matrix_name)
    read_times = zeros(1, 5);
    solve_times = zeros(1, 5);
    for i = 1:5
        [read_time, solve_time] = compute_cholesky_read_and_solve_time(matrix_name);
        read_times(i) = read_time;
        solve_times(i) = solve_time;
    end
end


function [] = compute_cholesky(matrix_name)
    [relative_error] = compute_cholesky_relative_error(matrix_name);
    [read_times, solve_times] = cholesky_times(matrix_name);
    disp([read_times, solve_times])
    writematrix(replace(string(cat(2, relative_error, cat(2, read_times, solve_times))), ".", ","), "results.txt", "WriteMode", "append", 'Delimiter','semi');
end

