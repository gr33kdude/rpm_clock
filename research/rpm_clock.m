x = linspace(0, 60, 10000);
y = base_rpm(x);
plot(x, y);
axis( [0, 60, 0, 13000] );

speeds = x;
rpms = rpm(speeds);

plot(x, y, speeds, rpms);
axis( [0, 60, 0, 13000] );