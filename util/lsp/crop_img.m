function [crop, U, V] = crop_img(im, fgMask, X, Y)
	% crop : cropped image
	% U : mapped X coordinate
	% V : mapped Y coordinate

	% compute the bounding box of fg
	imSize = size(fgMask);
	[fgY, fgX] = ind2sub(imSize, find(fgMask)); % This is different from X, Y

	h = max(fgY) - min(fgY) + 1; w = max(fgX) - min(fgX) + 1;

	marginRatio = 0.1;
	cmargin = max(h, w) * marginRatio;

	ch = h + 2 * cmargin; % h of crop patch
	cw = w + 2 * cmargin;

	s = 150.0 / max(ch, cw);
	ch = s * ch; cw = s * cw;
	tx = - s * (min(fgX) - cmargin) + 1; 
	% Translation in x, map (min(X) - margin) to 1, what will happen in it is smaller than 1
	ty = - s * (min(fgY) - cmargin) + 1; % translation in y

	A = [s  , 0  , 0; % Translate than scale
		 0  , s  , 0;
		 tx , ty , 1];


	T = maketform('affine', A);
	XData = [1, cw]; YData = [1, ch];
	crop = imtransform(im, T, 'XData', XData, 'YData', YData);

	% Mapping of landmark locations
	[U, V] = tformfwd(T, X, Y);
end