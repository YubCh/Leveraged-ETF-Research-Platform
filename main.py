from scripts import real_history, monte_carlo, draw_down_counts


def main():
    real_history.run()
    #real_history.run(start="2010-02-11")
    monte_carlo.run(n_paths=500)
    draw_down_counts.run()
 
 
if __name__ == "__main__":
    main()
