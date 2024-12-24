function r = decay(s, min_rpm = 2000, max_rpm = 13000, millis = 150)
  rpm_range = max_rpm - min_rpm;
  t = millis / 1000;
  
  base = min_rpm * t / rpm_range;
  rate = max_rpm * base;
  x_off = -base;
  
  decay_ = @(s) rate / (s - x_off);
  
  if isvector(s)
    r = arrayfun(decay_, s);
  endif
endfunction
