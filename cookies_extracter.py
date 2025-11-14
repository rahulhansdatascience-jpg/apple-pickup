import browser_cookie3
import json
import re
import sys
import os

def extract_user_agent():
    import subprocess, winreg

    try:
        # Get Chrome path
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")
        prog_id = winreg.QueryValueEx(key, "ProgId")[0]
        key2 = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, f"{prog_id}\\shell\\open\\command")
        chrome_cmd = winreg.QueryValueEx(key2, "")[0]

        chrome_path = chrome_cmd.split('"')[1]

        # Run Chrome to print UA
        result = subprocess.run(
            [chrome_path, "--headless", "--dump-dom", "https://www.apple.com"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        ua_match = re.search(r"User-Agent: (.+?)\n", result.stderr)
        if ua_match:
            return ua_match.group(1).strip()

    except:
        pass

    print("Unable to auto-detect User-Agent. Please manually copy from your browser.")
    return None


def extract_cookies():
    print("Extracting cookies from Chrome…")
    try:
        cj = browser_cookie3.chrome(domain_name=".apple.com")
        cookies = []

        for c in cj:
            if "apple.com" in c.domain:
                cookies.append(f"{c.name}={c.value}")

        cookie_string = "; ".join(cookies)

        with open("cookies.txt", "w") as f:
            f.write(cookie_string)

        return cookie_string

    except Exception as e:
        print("Error reading cookies:", e)
        return None


if __name__ == "__main__":
    cookies = extract_cookies()
    ua = extract_user_agent()

    if cookies:
        print("\nSaved cookies → cookies.txt")

    if ua:
        with open("ua.txt", "w") as f:
            f.write(ua)
        print("Saved user-agent → ua.txt")

    print("\nDone.")
