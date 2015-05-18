psu: parser.cpp scanner.cpp parser.hpp scanner.h driver.cpp driver.h expression.h
	gcc -o psu parser.cpp scanner.cpp driver.cpp -lstdc++ -g -O0

parser.cpp: parser.yy
	bison -oparser.cpp -d parser.yy

scanner.cpp:scanner.ll
	flex -oscanner.cpp -I scanner.ll

clean:
	rm -f *.o psu