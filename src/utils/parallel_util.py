from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import functools
from multiprocessing import cpu_count

class Parallel(object):
    """封装ProcessPoolExecutor进行并行任务执行操作"""

    def __init__(self, n_jobs=4, backend='process'):
        self.n_jobs = n_jobs
        self.backend = ProcessPoolExecutor
        if backend == 'process':
            self.backend = ProcessPoolExecutor
        else:
            self.backend = ThreadPoolExecutor
    def __call__(self, iterable):
        """为与joblib并行保持一致，内部使用ProcessPoolExecutor开始工作"""

        result = []

        def when_done(r):
            """ProcessPoolExecutor每一个进程结束后结果append到result中"""
            result.append(r.result())
        if self.n_jobs <= 0:
            # 主要为了适配 n_jobs = -1，joblib中启动cpu个数个进程并行执行
            self.n_jobs = cpu_count()
        if self.n_jobs == 1:
            # 如果只开一个进程，那么只在主进程(或当前运行的子进程)里运行，方便pdb debug且与joblib运行方式保持一致
            for jb in iterable:
                result.append(jb[0](*jb[1], **jb[2]))
        else:
            with self.backend(max_workers=min(self.n_jobs, cpu_count())) as pool:
                for jb in iterable:
                    # 这里iterable里每一个元素是delayed.delayed_function保留的tuple
                    future_result = pool.submit(jb[0], *jb[1], **jb[2])
                    future_result.add_done_callback(when_done)
        return result

def delayed(function):
    """
    将function通过functools.wraps及delayed_function进行保留，但不执行
    :param function:
    :return:
    """
    def delayed_function(*args, **kwargs):
        """将function以及参数返回为tuple，tuple[0]为原始function"""
        return function, args, kwargs

    try:
        delayed_function = functools.wraps(function)(delayed_function)
    except AttributeError:
        raise TypeError('wraps fails on some callable objects')
    return delayed_function