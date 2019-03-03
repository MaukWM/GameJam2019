import urllib.request
import hashlib


def submit_score(name, score):
    sha256 = hashlib.sha256()
    sha256.update((name + str(score) + "manySecureMuchSafeSalt").encode())
    hash = sha256.hexdigest()
    resp = urllib.request.urlopen(
        "http://lekkereframbozen.student.utwente.nl/submit_2019.php?name=%s&score=%d&hash=%s" % (name, score, hash)
    ).read()
    if resp != b'400 OK':
        print("Error submitting scores: %s"%resp)
    else:
        print("Score successfully submitted to server :)")


if __name__ == "__main__":
    submit_score("HoiDitIsEenKutLangeNaamWatDusBestKutIs", 123)
