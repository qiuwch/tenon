function blur = gaussblur(im, sz, sigma)
	% What is the parameter of motion blur?
	H = fspecial('gaussian', sz, sigma);
	blur = imfilter(im,H,'replicate');
end
