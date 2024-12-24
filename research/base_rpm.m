function r = base_rpm(s)
  max_rpm = 13000 - 1000 + 1000;
  min_rpm = 1000;
  steepness = 0.08;
  x_off = 30;
  
  base_rpm_ = @(s) (max_rpm-min_rpm) / (1 + exp(-steepness*(s-x_off)));
  
  b_rpm = @(s) base_rpm_(s) - base_rpm_(0);
  if (isvector(s))
    r = arrayfun(b_rpm, s);
  endif
endfunction