im = imread('/q/cache/render_output/imgs/im0001.png');
imshow(im);
A = csvread('/q/cache/render_output/joint-PC-MATLAB.csv');
X = A(:,1:2:27);
Y = A(:,2:2:28);
hold on;
plot(X(1,:), Y(1,:), '*');