function blur = motionblur(im, vec)
	% What is the parameter of motion blur?
	H = fspecial('motion',vec(1),vec(2));
	blur = imfilter(im,H,'replicate');
end
