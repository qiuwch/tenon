im = imread('/q/cache/render_output/imgs/0000.png');
imshow(im);
A = csvread('/q/cache/render_output/joint.csv');
X = A(:,1:2:27);
Y = A(:,2:2:28);
hold on;
plot(X(1,:), Y(1,:), '*');