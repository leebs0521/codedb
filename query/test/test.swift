//
// Created by kojirof on 2018-11-19.
// Copyright (c) 2018 Gumob. All rights reserved.
//

import Foundation

public class Punycode {

    /// Punycode RFC 3492
    /// See https://www.ietf.org/rfc/rfc3492.txt for standard details

    private let base: Int = 36
    private let tMin: Int = 1
    private let tMax: Int = 26
    private let skew: Int = 38
    private let damp: Int = 700
    private let initialBias: Int = 72
    private let initialN: Int = 128

    /// RFC 3492 specific
    private let delimiter: Character = "-"
    private let lowercase: ClosedRange<Character> = "a"..."z"
    private let digits: ClosedRange<Character> = "0"..."9"
    private let lettersBase: UInt32 = Character("a").unicodeScalars.first!.value
    private let digitsBase: UInt32 = Character("0").unicodeScalars.first!.value

    /// IDNA
    private let ace: String = "xn--"

    private func adaptBias(_ delta: Int, _ numberOfPoints: Int, _ firstTime: Bool) -> Int {
        var delta: Int = delta
        if firstTime {
            delta /= damp
        } else {
            delta /= 2
        }
        delta += delta / numberOfPoints
        var k: Int = 0
        while delta > ((base - tMin) * tMax) / 2 {
            delta /= base - tMin
            k += base
        }
        return k + ((base - tMin + 1) * delta) / (delta + skew)
    }

    /// Maps a punycode character to index
    private func punycodeIndex(for character: Character) -> Int? {
        if lowercase.contains(character) {
            return Int(character.unicodeScalars.first!.value - lettersBase)
        } else if digits.contains(character) {
            return Int(character.unicodeScalars.first!.value - digitsBase) + 26 /// count of lowercase letters range
        } else {
            return nil
        }
    }

    /// Maps an index to corresponding punycode character
    private func punycodeValue(for digit: Int) -> Character? {
        guard digit < base else { return nil }
        if digit < 26 {
            return Character(UnicodeScalar(lettersBase.advanced(by: digit))!)
        } else {
            return Character(UnicodeScalar(digitsBase.advanced(by: digit - 26))!)
        }
    }

    /// Decodes punycode encoded string to original representation
    ///
    /// - Parameter punycode: Punycode encoding (RFC 3492)
    /// - Returns: Decoded string or nil if the input cannot be decoded


    /// Encodes string to punycode (RFC 3492)
    ///
    /// - Parameter input: Input string
    /// - Returns: Punycode encoded string
    public func encodePunycode(_ input: Substring) -> String? {
        var n: Int = initialN
        var delta: Int = 0
        var bias: Int = initialBias
        var output: String = ""
        for scalar in input.unicodeScalars {
            if scalar.isASCII {
                let char = Character(scalar)
                output.append(char)
            } else if !scalar.isValid {
                return nil /// Encountered a scalar out of acceptable range
            }
        }
        var handled: Int = output.count
        let basic: Int = handled
        if basic > 0 {
            output.append(delimiter)
        }
        while handled < input.unicodeScalars.count {
            var minimumCodepoint: Int = 0x10FFFF
            for scalar: Unicode.Scalar in input.unicodeScalars {
                if scalar.value < minimumCodepoint && scalar.value >= n {
                    minimumCodepoint = Int(scalar.value)
                }
            }
            delta += (minimumCodepoint - n) * (handled + 1)
            n = minimumCodepoint
            for scalar: Unicode.Scalar in input.unicodeScalars {
                if scalar.value < n {
                    delta += 1
                } else if scalar.value == n {
                    var q: Int = delta
                    var k: Int = base
                    while true {
                        let t = k <= bias ? tMin : (k >= bias + tMax ? tMax : k - bias)
                        if q < t {
                            break
                        }
                        guard let character: Character = punycodeValue(for: t + ((q - t) % (base - t))) else { return nil }
                        output.append(character)
                        q = (q - t) / (base - t)
                        k += base
                    }
                    guard let character: Character = punycodeValue(for: q) else { return nil }
                    output.append(character)
                    bias = adaptBias(delta, handled + 1, handled == basic)
                    delta = 0
                    handled += 1
                }
            }
            delta += 1
            n += 1
        }

        return output
    }

    /// Returns new string containing IDNA-encoded hostname
    ///
    /// - Returns: IDNA encoded hostname or nil if the string can't be encoded
    public func encodeIDNA(_ input: Substring) -> String? {
        let parts: [Substring] = input.split(separator: ".")
        var output: String = ""
        for part: Substring in parts {
            if output.count > 0 {
                output.append(".")
            }
            if part.rangeOfCharacter(from: CharacterSet.urlHostAllowed.inverted) != nil {
                guard let encoded: String = part.lowercased().punycodeEncoded else { return nil }
                output += ace + encoded
            } else {
                output += part
            }
        }
        return output
    }

    /// Returns new string containing hostname decoded from IDNA representation
    ///
    /// - Returns: Original hostname or nil if the string doesn't contain correct encoding
    public func decodedIDNA(_ input: Substring) -> String? {
        let parts: [Substring] = input.split(separator: ".")
        var output: String = ""
        for part: Substring in parts {
            if output.count > 0 {
                output.append(".")
            }
            if part.hasPrefix(ace) {
                guard let decoded: String = part.dropFirst(ace.count).punycodeDecoded else { return nil }
                output += decoded
            } else {
                output += part
            }
        }
        return output
    }
}
