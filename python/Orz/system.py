
def cpu_number():
    import multiprocessing 
    try:
        return multiprocessing.cpu_count()
    except NotImplementedError:
        return 1


