### ToKEYdemaru
A proof-of-concept Python script for generating and validating public-private keypairs that utilize Pokemon battling as a sort of hashing function.

### Usage
Make sure to install the following packages with pip:
`pokemon_formats`
`pokebase`

Run the program with either an IDE or through the command line.  
You will be presented with three options.  Options 1 and 2 let you generate a keypair, and option 3 is for validating keypairs.


### Current limitations
Other than STAB, natures, type effectiveness, damage, and protect, most battle mechanics have not yet been implemented.  Additionally, to make sure the game states are deterministic, all mechanics based on randomness are unimplemented.
Game-specific gimmicks are also not implemented (Gmax, Tera, etc.)

Please don't use this in anything that needs actually secure keys.


