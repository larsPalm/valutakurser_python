from stresstest import get_data,insert_data
from atmoicInteger import AtomicInteger
import threading
import multiprocessing
import matplotlib.pyplot as plt


if __name__ == '__main__':
    score = []
    labels = ['fetching data', 'insert data', 'hybrid']
    threads = multiprocessing.cpu_count()
    for x in range(3):
        all_test = []
        for y in range(7):
            ai1 = AtomicInteger()
            ai2 = AtomicInteger()
            if x == 0:
                processes = [threading.Thread(target=get_data, args=(ai1, ai2)) for _ in range(threads)]
                for p in processes:
                    p.start()
                for p in processes:
                    p.join()
            if x == 1:
                processes = [threading.Thread(target=insert_data, args=(ai1, ai2)) for _ in range(threads)]
                for p in processes:
                    p.start()
                for p in processes:
                    p.join()
            if x == 2:
                processes = [
                    threading.Thread(target=insert_data, args=(ai1, ai2)) if x % 2 == 0 else threading.Thread(
                        target=get_data, args=(ai1, ai2)) for x in range(threads)]
                for p in processes:
                    p.start()
                for p in processes:
                    p.join()
            all_test.append(ai1.get_value()/ai2.get_value())
        score.append(all_test)
    x_values = list(range(7))
    teller = 0
    for key in score:
        plt.plot(x_values, score[teller], label=labels[teller])
        teller += 1
    #plt.title('percentage of sucessful attempts')
    #plt.title('percentage of sucessful attempts for SQLite')
    #plt.title('percentage of sucessful attempts for PostgreSQL')
    plt.legend()
    plt.xlim([x_values[0], x_values[-1]])
    #plt.savefig('sqlite.png')
    #plt.savefig('postgresql.png')
    plt.show()
