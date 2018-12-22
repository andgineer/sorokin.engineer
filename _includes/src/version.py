def version():
    try:
        return open('build_timestamp', 'r').read().strip()
    except:
        return None


if __name__ == '__main__':
    print(version())
