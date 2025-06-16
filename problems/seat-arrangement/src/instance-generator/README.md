# Generator for the Seating Arrangement Problem

Run for details on how to run the generator:
```
python seat_arr_generator.py --help
```
The following options are available:
```
  -h, --help  show this help message and exit
  -o O        output folder (default: ../../../data/instances/)
  -G G        number of guests (default: 10)
  -T T        number of tables (default: 3)
  -l L        minimum number of guests per table (default: 2)
  -u U        maximum number of guests per table (default: 5)
  -L L        number of labels (default: 10)
  -d D        maximum number of disagreements (default: 0)
  -W W        maximum label weight (between 1 and 10) (default: 10)

```
Example:
```
python seat_arr_generator.py -o ../../../data/instances/ -G 10 -T 3 -l 2 -u 5 -L 10 -d 0 -W 10
```
This command will generate the file `../../../data/instances/sap_10G_3T_2l_5u_10L_0d_10w.in` with an instance with 10 guests, 3 tables with 2 to 5 guests, 10 labels with weights between 1 and 10.