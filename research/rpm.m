function r = rpm(s)
  max_rpm = 13000 - 1000 + 1000;
  num_gears = 9;

  #x_off = @(speed_range) floor(speed_range * 7/8);
  speed_interval = 60 / num_gears;
  min_speed = @(s) floor(s / speed_interval) * speed_interval;
  max_speed = @(s)  ceil(s / speed_interval) * speed_interval;
  b_rpm = @(s) base_rpm(min_speed(s));
  B_rpm = @(s) base_rpm(max_speed(s));
  
  max_off = 13/16;
  min_off = 1/2;
  
  gear = @(s) ceil(s/speed_interval);
  off  = @(s) min_off + (max_off - min_off) * gear(s)/num_gears;
  
  x_off = @(s) speed_interval * off(s); #- floor(speed_interval*5/16);
  #x_off = @(s) speed_interval / 2; #- floor(speed_interval*5/16);
  steepness = @(s) (0.85 - (1/num_gears * floor(s/speed_interval)) * 0.7);
  
  rpm_range = @(s) max_rpm - b_rpm(s);

  rpm_logistic  = @(s) (rpm_range(s) / (1 + exp(-steepness(s) * (s - min_speed(s) - x_off(s)))));
  rpm_quadratic = @(s) (rpm_range(s)/(1.1*speed_interval)^2) * (s - min_speed(s) + speed_interval/10) ^ 2;
  
  rpm_h = @(s) b_rpm(s) + rpm_logistic(s);
  
  millis = 150;
  t = millis / 1000;
  m = rpm_h(min_speed(s));
  M = rpm_h(s + t);
  if ((s - m) < t)
    r = decay(s, m, M, millis);
  else
    if isvector(s)
      r = arrayfun(rpm_h, s);
    endif
  endif
endfunction