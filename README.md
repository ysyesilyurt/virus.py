# virus.py
Is it possible to `hack` *covidiots* to stop them spreading [Covid-19](https://www.wikiwand.com/en/Coronavirus_disease_2019)?

## How?
1- Copies an encrypted version of itself using [otp](https://www.wikiwand.com/en/One-time_pad) (along with its decryption key ofc)

2- Infects all the python scripts underneath its sandbox, i.e. root directory (appends itself and then also appends the hash value of the infected version of the file to make sure injected virus remains there, i.e. guarded against all kind of modifications, and not to infect an already infected file twice)

3- Executes its payload, namely displays the current coronavirus stats (using [this](https://corona-stats.online/?top=15) API) to prevent that victim *covidiot* to stop spreading the disease.

4- And then when an infected script gets executed, all the steps gets repeated from step-1...

#### Caution: if you want to try it make sure to isolate this notorious (:blush:) virus.py from your other valuable python scripts, you may want to create a sandbox folder and try it in there.
