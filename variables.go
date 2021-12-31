package main 

import (
	"encoding/csv"
	"os"
	"regexp"
	"fmt"
	"io"
)

var validVariable = regexp.MustCompile(`^\$[A-Za-z0-9_]+`)

// gets all the variables from a logger file on stdin,
// prints them uniquely to stdout
func main() {
	variables := make(map[string]bool)
	r := csv.NewReader(os.Stdin)
	// space sep
	r.Comma = ' '
	// allow variable row lengths
	r.FieldsPerRecord = -1 

	for {
		record, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}

		inputs := record[3:]
		for _, input := range inputs {
			if validVariable.MatchString(input) {
				variables[input] = true
			}
		}
	}

	for variable, _ := range variables {
		fmt.Fprintln(os.Stdout, variable)
	}
}