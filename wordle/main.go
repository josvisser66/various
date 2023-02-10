package main

import (
	"fmt"
	"os"
	"strings"
)

const length = 5

type set[T comparable] map[T]struct{}

func newSet[T comparable]() set[T] {
	return make(map[T]struct{})
}

func (s set[T]) add(t T) {
	s[t] = struct{}{}
}

func (s set[T]) remove(t T) {
	delete(s, t)
}

func (s set[T]) has(t T) bool {
	_, ok := s[t]
	return ok
}

func (s set[T]) forEach(f func(t T)) {
	for el := range s {
		f(el)
	}
}

func readWordList() []string {
	b, err := os.ReadFile("/usr/share/dict/words")
	if err != nil {
		panic(err)
	}

	a := strings.Split(string(b), "\n")

	var result []string

	for _, word := range a {
		if len(word) == length {
			result = append(result, strings.ToLower(word))
		}
	}

	return result
}

func readAnswer(try string) string {
	var answer string

outer:
	for {
		fmt.Printf("My guess: %s\n> ", try)
		_, err := fmt.Scanf("%s", &answer)
		if err != nil {
			fmt.Println(err)
			continue
		}

		if len(answer) != length {
			fmt.Println("Please enter five characters  x == no match, y == yellow, g = green")
			continue
		}

		for _, c := range answer {
			if c != 'x' && c != 'y' && c != 'g' {
				fmt.Println("Please enter five characters  x == no match, y == yellow, g = green")
				continue outer
			}
		}

		return answer
	}
}

func main() {
	var canBe [length]set[rune]
	hasToContain := newSet[rune]()

	for i := 0; i < length; i++ {
		canBe[i] = newSet[rune]()
	}

	words := readWordList()

	for _, word := range words {
		for i := 0; i < length; i++ {
			canBe[i].add(rune(word[i]))
		}
	}

	try := "sweat"

	for len(words) > 1 {
		answer := readAnswer(try)

		for i, c := range answer {
			kar := rune(try[i])
			switch c {
			case 'g':
				canBe[i] = newSet[rune]()

				canBe[i].add(kar)
				hasToContain.add(kar)
			case 'y':
				canBe[i].remove(kar)
				hasToContain.add(kar)
			case 'x':
				for j := 0; j < length; j++ {
					canBe[j].remove(kar)
				}
				hasToContain.remove(kar)
			default:
				panic("Unexpected character")
			}
		}

		var newWords []string

	outer:
		for _, word := range words {
			for i, c := range word {
				if !canBe[i].has(c) {
					fmt.Printf("reject %s\n", word)
					continue outer
				}
			}

			n := 0

		inner:
			for c := range hasToContain {
				for _, d := range word {
					if c == d {
						n++
						continue inner
					}
				}
			}

			if n == len(hasToContain) {
				newWords = append(newWords, word)
			} else {
				fmt.Printf("reject %s\n", word)
			}
		}

		words = newWords

		fmt.Println("len(words) ==", len(words))
		fmt.Print("hasToContain ")
		hasToContain.forEach(func(c rune) { fmt.Printf("%c ", c) })
		fmt.Println()

		for i := 0; i < length; i++ {
			fmt.Printf("%d: ", i)
			canBe[i].forEach(func(c rune) { fmt.Printf("%c ", c) })
			fmt.Println()
		}

		try = words[0]
	}

	fmt.Println("It has got to be", try)
}
