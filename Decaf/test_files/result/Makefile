compile:
	as -o source.o source.s
	ld -macosx_version_min 11.0.0 -o source source.o -lSystem -syslibroot `xcrun -sdk macosx --show-sdk-path` -e _main -arch arm64