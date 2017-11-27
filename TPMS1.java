package start;

import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;

import org.python.core.PyInstance;
import org.python.util.PythonInterpreter;
import org.python.core.PyObject;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.text.SimpleDateFormat;
import java.util.Date;
import javax.swing.border.TitledBorder;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

// follow the below link
//https://stackoverflow.com/questions/804466/how-do-i-create-executable-java-program
public class TPMS1 extends JFrame {

    PythonInterpreter interpreter = null;

    // Auto panel (Main)
    JPanel autoPanel = new JPanel();

    // Layouts for search function (Main Panel)
    JPanel searchPanel = new JPanel();

    // Default lay out
    JPanel keyBoardPanel = new JPanel();

    // After search the data
    JPanel searchDataPanel = new JPanel();

    Timer timer_auto;

    Timer timer_search;

    String numberString = "";

    JTextField jtf = new JTextField();
    JButton b1 = new JButton("1");
    JButton b2 = new JButton("2");
    JButton b3 = new JButton("3");
    JButton b4 = new JButton("4");
    JButton b5 = new JButton("5");
    JButton b6 = new JButton("6");
    JButton b7 = new JButton("7");
    JButton b8 = new JButton("8");
    JButton b9 = new JButton("9");
    JButton bstart = new JButton("Start");
    JButton b0 = new JButton("0");

    JButton bclear = new JButton("Clear");

    Font tp_font = new Font("Arial", Font.PLAIN, 30);
    Font tpHeader_font = new Font("Arial", Font.PLAIN, 15).deriveFont(Font.BOLD);

    public static void main(String[] args) {
        //Create and set up the window.
        TPMS tpms = new TPMS();
        tpms.initUI();
    }

    public void initUI() {

        setBackground(Color.BLACK);
        setTitle("Tyre Pressure & Temperature");

        // Create two tabs
        // 1) Auto - update, 2) Search
        // Create Auto-Update tab
        autoPanel.setLayout(new BorderLayout());

        // Create Search tab
        searchPanel.setLayout(new BorderLayout());

        // Add two tabs
        JTabbedPane tp = new JTabbedPane();
        tp.add("Automatic", autoPanel);
        tp.add("Search", searchPanel);

        // Add the tabs to screen
        getContentPane().add(tp);

        tp.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                System.out.println("Tab: " + tp.getSelectedIndex());
                if (tp.getSelectedIndex() == 1) {
                    // Search
                    System.out.println("Stoping auto timer");
                    System.out.println("Start search timer");
                    timer_auto.stop();
                    // Visible the keyboard panel
                    numberString = "";
                    jtf.setText("");
                    keyBoardPanel.setVisible(true);
                } else {
                    // Auto
                    if (null != timer_search) {
                        timer_search.stop();
                    }
                    createAutoScreen();
                    System.out.println("Start auto timer");
                    refreshAutoScreen();
                }
            }
        });

        // Create search screen
//        createSearchScreen(searchPanel);
        // Create Auto Screen - By Default
        createAutoScreen();
        refreshAutoScreen();

        keyBoardPanel.setLayout(new BorderLayout());

        addDefaultSearchPanel(keyBoardPanel);
        keyBoardPanel.setVisible(true);
        searchPanel.add(keyBoardPanel);

        // Adding to JFrame
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setExtendedState(JFrame.MAXIMIZED_BOTH);
        setUndecorated(true);
        setVisible(true);
        pack();
    }

    public void createSearchScreen() {

        System.out.println("createSearchScreen " + jtf.getText());
        Connection conn = connectToSQLite();
        if (null != jtf.getText() && jtf.getText().trim().length() >= 4) {
            try {
                Statement stmt = conn.createStatement();
                String sql = "SELECT * FROM DeviceDetails where vehName like '%" + jtf.getText() + "%'";
                ResultSet rs = stmt.executeQuery(sql);
                if (rs.next()) {
                    String rfuid = rs.getString("RFUID");
                    String btuid = rs.getString("BUID");
                    if (null != rfuid && rfuid.trim().length() > 0 && null != btuid && btuid.trim().length() > 0) {
                        // Call the python program
                        TPMS1 ie = new TPMS1();
                        ie.execfile("hello.py");
                        String result = ie.getTPMSDetials(rfuid);
                        JOptionPane.showMessageDialog(searchPanel, "Body message " + result, "Warning", JOptionPane.PLAIN_MESSAGE);

                        refreshSearchScreen(rs.getString("vehName"));
                    }
                } else {
                    System.out.println("Vehicle not found with " + jtf.getText());
                    JOptionPane.showMessageDialog(searchPanel, "Vehicle not found", "Warning", JOptionPane.PLAIN_MESSAGE);
                }
            } catch (Exception e) {
                e.printStackTrace();
            } finally {
                try {
                    if (conn != null) {
                        conn.close();
                    }
                } catch (Exception exp1) {
                    exp1.printStackTrace();
                }
            }
        } else {
            JOptionPane.showMessageDialog(searchPanel, "Please enter 4 digit vehicle number", "Warning", JOptionPane.PLAIN_MESSAGE);
        }
    }

    public void createSearchPanel(String vehName) {
        Connection conn = connectToSQLite();
        try {
            System.out.println("start.TPMS.createSearchPanel() " + new Date());
            keyBoardPanel.setVisible(false);
            searchDataPanel.setLayout(new BorderLayout());
            JPanel vehNamePanle = new JPanel(new GridLayout(1, 3));
            vehNamePanle.setBorder(BorderFactory.createLineBorder(Color.black));
            JButton bstop = new JButton("Stop");
            bstop.setFont(new Font("Arial", Font.PLAIN, 40));
//            bstop.setBackground(Color.RED);
            bstop.setForeground(Color.RED);
            vehNamePanle.add(bstop);

            // Stop button action listerner
            bstop.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    timer_search.stop();
                    numberString = "";
                    jtf.setText("");
                    searchDataPanel.setVisible(false);
                    keyBoardPanel.setVisible(true);
                }
            });

            JLabel lVehName_label = new JLabel(vehName);
            lVehName_label.setHorizontalAlignment(SwingConstants.CENTER);
            lVehName_label.setFont(new Font("Arial", Font.PLAIN, 40));

            vehNamePanle.add(lVehName_label);

            JLabel dateTime_label = new JLabel();
            dateTime_label.setHorizontalAlignment(SwingConstants.RIGHT);
            dateTime_label.setFont(new Font("Arial", Font.PLAIN, 20));

            vehNamePanle.add(dateTime_label);

            bstop.setPreferredSize(new Dimension(200, 100));
            searchDataPanel.add(vehNamePanle, BorderLayout.NORTH);

            try {
                // Connect to DB, get the latest data
                Statement stmt = conn.createStatement();
                String sql = "SELECT vehId FROM Latest_data where count <= 5 order by device_date_time DESC limit 1;";
                ResultSet rs = stmt.executeQuery(sql);
                if (rs.next()) {
                    long vehId = rs.getLong("vehId");
                    sql = "SELECT * FROM Latest_data where vehId = " + vehId;
                    ResultSet rs1 = stmt.executeQuery(sql);
                    String fl_temp = null;
                    String fr_temp = null;
                    String rlo_temp = null;
                    String rli_temp = null;
                    String rri_temp = null;
                    String rro_temp = null;

                    String fl_pressure = null;
                    String fr_pressure = null;
                    String rlo_pressure = null;
                    String rli_pressure = null;
                    String rri_pressure = null;
                    String rro_pressure = null;
                    long dateTime = 0;
                    while (rs1.next()) {
                        try {
                            dateTime = rs1.getLong("device_date_time");
                            if (rs1.getString("location").equalsIgnoreCase("01")
                                    || rs1.getString("location").equalsIgnoreCase("FL")) {
                                fl_temp = rs1.getString("temp");
                                fl_pressure = rs1.getString("pressure");
                            } else if (rs1.getString("location").equalsIgnoreCase("02")
                                    || rs1.getString("location").equalsIgnoreCase("FR")) {
                                fr_temp = rs1.getString("temp");
                                fr_pressure = rs1.getString("pressure");
                            } else if (rs1.getString("location").equalsIgnoreCase("03")
                                    || rs1.getString("location").equalsIgnoreCase("RLO")) {
                                rlo_temp = rs1.getString("temp");
                                rlo_pressure = rs1.getString("pressure");
                            } else if (rs1.getString("location").equalsIgnoreCase("04")
                                    || rs1.getString("location").equalsIgnoreCase("RLI")) {
                                rli_temp = rs1.getString("temp");
                                rli_pressure = rs1.getString("pressure");
                            } else if (rs1.getString("location").equalsIgnoreCase("05")
                                    || rs1.getString("location").equalsIgnoreCase("RRI")) {
                                rri_temp = rs1.getString("temp");
                                rri_pressure = rs1.getString("pressure");
                            } else if (rs1.getString("location").equalsIgnoreCase("06")
                                    || rs1.getString("location").equalsIgnoreCase("RRO")) {
                                rro_temp = rs1.getString("temp");
                                rro_pressure = rs1.getString("pressure");
                            }
                        } catch (Exception ex) {
                            ex.printStackTrace();
                        }
                    }
                    if (dateTime > 0) {
                        SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
                        dateTime_label.setText(sdf.format(dateTime));
                    }
                    JPanel bottomMainPanel = createBottomPanel(fl_temp, fl_pressure, fr_temp,
                            fr_pressure, rlo_temp, rlo_pressure, rli_temp, rli_pressure,
                            rri_temp, rri_pressure, rro_temp, rro_pressure);

                    searchDataPanel.add(bottomMainPanel, BorderLayout.CENTER);
                }
            } catch (Exception exp) {
                exp.printStackTrace();
            }
            searchPanel.add(searchDataPanel);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (conn != null) {
                    conn.close();
                }
            } catch (Exception exp1) {
                exp1.printStackTrace();
            }
        }
    }

    public void addDefaultSearchPanel(JPanel keyBoardPanel) {
        System.out.println("start.TPMS.addDefaultSearchPanel()");

        keyBoardPanel.setLayout(new BorderLayout());
        // Create key board
        JPanel headerPanel_search = new JPanel(new GridLayout(4, 3));
        b1.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b1);
        b2.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b2);
        b3.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b3);
        b4.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b4);
        b5.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b5);
        b6.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b6);
        b7.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b7);
        b8.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b8);
        b9.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b9);
        bstart.setFont(new Font("Arial", Font.PLAIN, 35));
        headerPanel_search.add(bstart);
        b0.setFont(new Font("Arial", Font.PLAIN, 50));
        headerPanel_search.add(b0);
        bclear.setFont(new Font("Arial", Font.PLAIN, 40));
        headerPanel_search.add(bclear);

        ButtonListener listener = new ButtonListener();

        b0.addActionListener(listener);
        b1.addActionListener(listener);
        b2.addActionListener(listener);
        b3.addActionListener(listener);
        b4.addActionListener(listener);
        b5.addActionListener(listener);
        b6.addActionListener(listener);
        b7.addActionListener(listener);
        b8.addActionListener(listener);
        b9.addActionListener(listener);
        bstart.addActionListener(listener);
        bclear.addActionListener(listener);

        jtf.setHorizontalAlignment(SwingConstants.CENTER);
        jtf.setPreferredSize(new Dimension(200, 150));
        jtf.setFont(new Font("Arial", Font.PLAIN, 50));
        keyBoardPanel.add(jtf, BorderLayout.NORTH);
        keyBoardPanel.add(headerPanel_search, BorderLayout.CENTER);

        System.out.println("Created key board");
    }

    class ButtonListener implements ActionListener {

        @Override
        public void actionPerformed(ActionEvent e) {
            if (e.getSource() == b1) {
                numberString += "1";
            } else if (e.getSource() == b2) {
                numberString += "2";
            } else if (e.getSource() == b3) {
                numberString += "3";
            } else if (e.getSource() == b4) {
                numberString += "4";
            } else if (e.getSource() == b5) {
                numberString += "5";
            } else if (e.getSource() == b6) {
                numberString += "6";
            } else if (e.getSource() == b7) {
                numberString += "7";
            } else if (e.getSource() == b8) {
                numberString += "8";
            } else if (e.getSource() == b9) {
                numberString += "9";
            } else if (e.getSource() == b0) {
                numberString += "0";
            } else if (e.getSource() == bclear) {
                numberString = "";
            } else if (e.getSource() == bstart) {
//                searchDataPanel.setVisible(true);
//                keyBoardPanel.setVisible(false);
                createSearchScreen();
            }
            jtf.setText(numberString);
        }
    }

    public void refreshAutoScreen() {
        timer_auto = new Timer(0, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                createAutoPanel();
            }
        });
        timer_auto.setRepeats(true);
        // 30 sec once
        timer_auto.setDelay(10 * 1000);
        timer_auto.start();
    }

    public void refreshSearchScreen(String vehName) {
        timer_search = new Timer(0, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                createSearchPanel(vehName);
            }
        });
        timer_search.setRepeats(true);
        // 30 sec once
        timer_search.setDelay(10 * 1000);
        timer_search.start();
    }

    public TPMS1() {
        PythonInterpreter.initialize(System.getProperties(),
                System.getProperties(), new String[0]);
        this.interpreter = new PythonInterpreter();
    }

    void execfile(final String fileName) {
        this.interpreter.execfile(fileName);
    }

    public String getTPMSDetials(String rfid) {

        PyObject str = this.interpreter.eval("repr(run('" + rfid + "'))");
        return str.toString();
    }

    PyInstance createClass(final String className, final String opts) {
        return (PyInstance) this.interpreter.eval(className + "(" + opts + ")");
    }

    public void createAutoScreen() {
        System.out.println("start.TPMS.createAutoScreen()");
        autoPanel.setLayout(new BorderLayout());
    }

    private void createAutoPanel() {

        System.out.println("start.TPMS.createAutoPanel() " + new Date());
        // Connect to DB, get the latest data
        JLabel lVehName = new JLabel();
        lVehName.setPreferredSize(new Dimension(200, 70));
        lVehName.setHorizontalAlignment(SwingConstants.CENTER);
        lVehName.setFont(new Font("Arial", Font.PLAIN, 40));
        autoPanel.add(lVehName, BorderLayout.NORTH);
        Connection conn = connectToSQLite();
        try {
            Statement stmt = conn.createStatement();
            String sql = "SELECT vehId FROM Latest_data where count <= 5 order by device_date_time DESC limit 1;";
            ResultSet rs = stmt.executeQuery(sql);
            if (rs.next()) {
                long vehId = rs.getLong("vehId");
                sql = "SELECT * FROM Latest_data where vehId = " + vehId;
                ResultSet rs1 = stmt.executeQuery(sql);
                String fl_temp = null;
                String fr_temp = null;
                String rlo_temp = null;
                String rli_temp = null;
                String rri_temp = null;
                String rro_temp = null;

                String fl_pressure = null;
                String fr_pressure = null;
                String rlo_pressure = null;
                String rli_pressure = null;
                String rri_pressure = null;
                String rro_pressure = null;
                String vehName = null;
                long dateTime = 0;
                while (rs1.next()) {
                    try {
                        vehName = "" + rs1.getInt("vehId");
                        dateTime = rs1.getLong("device_date_time");
                        if (rs1.getString("location").equalsIgnoreCase("01")
                                || rs1.getString("location").equalsIgnoreCase("FL")) {
                            fl_temp = rs1.getString("temp");
                            fl_pressure = rs1.getString("pressure");
                        } else if (rs1.getString("location").equalsIgnoreCase("02")
                                || rs1.getString("location").equalsIgnoreCase("FR")) {
                            fr_temp = rs1.getString("temp");
                            fr_pressure = rs1.getString("pressure");
                        } else if (rs1.getString("location").equalsIgnoreCase("03")
                                || rs1.getString("location").equalsIgnoreCase("RLO")) {
                            rlo_temp = rs1.getString("temp");
                            rlo_pressure = rs1.getString("pressure");
                        } else if (rs1.getString("location").equalsIgnoreCase("04")
                                || rs1.getString("location").equalsIgnoreCase("RLI")) {
                            rli_temp = rs1.getString("temp");
                            rli_pressure = rs1.getString("pressure");
                        } else if (rs1.getString("location").equalsIgnoreCase("05")
                                || rs1.getString("location").equalsIgnoreCase("RRI")) {
                            rri_temp = rs1.getString("temp");
                            rri_pressure = rs1.getString("pressure");
                        } else if (rs1.getString("location").equalsIgnoreCase("06")
                                || rs1.getString("location").equalsIgnoreCase("RRO")) {
                            rro_temp = rs1.getString("temp");
                            rro_pressure = rs1.getString("pressure");
                        }
                    } catch (Exception ex) {
                        ex.printStackTrace();
                    }
                }
                JPanel bottomMainPanel = createBottomPanel(fl_temp, fl_pressure, fr_temp,
                        fr_pressure, rlo_temp, rlo_pressure, rli_temp, rli_pressure,
                        rri_temp, rri_pressure, rro_temp, rro_pressure);

//                bottomPanel_auto = new JPanel(new GridLayout(2, 3));
//                bottomPanel_auto.add(bottomMainPanel);
//                bottomPanel_auto.setVisible(true);
//
//                splitPaneV_auto.setRightComponent(bottomPanel_auto);
                autoPanel.add(bottomMainPanel, BorderLayout.CENTER);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (conn != null) {
                    conn.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

    }

    private static JLabel getPressureLabel() {

        JLabel pressure_label = new JLabel("Pressure");
        try {
            BufferedImage pressure_img = ImageIO.read(new File("pressure.png"));
            Image pressure_bimg = pressure_img.getScaledInstance(60, 60, Image.SCALE_SMOOTH);
            ImageIcon pressure_icon = new ImageIcon(pressure_bimg);
            pressure_label = new JLabel("", pressure_icon, JLabel.LEFT);

        } catch (Exception e) {
            e.printStackTrace();
        }
        return pressure_label;
    }

    private static JLabel getTempLabel() {

        JLabel label = new JLabel("Temperature");
        try {
            BufferedImage temp_img = ImageIO.read(new File("temp.png"));
            Image temp_bimg = temp_img.getScaledInstance(70, 80, Image.SCALE_SMOOTH);
            ImageIcon temp_icon = new ImageIcon(temp_bimg);
            label = new JLabel("", temp_icon, JLabel.LEFT);

        } catch (Exception e) {
            e.printStackTrace();
        }
        return label;
    }

    public JPanel createBottomPanel(String FLTemp, String FLPressure,
            String FRTemp, String FRPressure, String RLOTemp, String RLOPressure,
            String RLITemp, String RLIPressure, String RRITemp, String RRIPressure,
            String RROTemp, String RROPressure) {

        JPanel bottomMainPanel = new JPanel(new GridLayout(1, 3));

        // For gaps between Temp & Pressure
        GridLayout sizeLayout = new GridLayout(2, 2, 10, 10);
        try {
            // Left side values
            JPanel leftPanel = new JPanel();
            BoxLayout leftLayout = new BoxLayout(leftPanel, BoxLayout.Y_AXIS);
            leftPanel.setLayout(leftLayout);

            JPanel panel11 = new JPanel();
            panel11.setBorder(BorderFactory.createTitledBorder(null, "Front Left", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

            JLabel fl_pressure_value = new JLabel("<html><font color='red'>" + FLPressure + "</font></html>");
            fl_pressure_value.setFont(tp_font);
            JLabel fl_temp_value = new JLabel(FLTemp);
            fl_temp_value.setFont(tp_font);
            JPanel fl_panel = new JPanel(sizeLayout);
            fl_panel.add(getPressureLabel());
            fl_panel.add(fl_pressure_value);
            fl_panel.add(getTempLabel());
            fl_panel.add(fl_temp_value);

            panel11.add(fl_panel);

            leftPanel.add(panel11);

            JPanel panel12 = new JPanel();
            panel12.setBorder(BorderFactory.createTitledBorder(null, "Rear Left Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

            JLabel rlo_pressure_value = new JLabel("<html><font color='red'>" + RLOPressure + "</font></html>");
            rlo_pressure_value.setFont(tp_font);
            JLabel rlo_temp_value = new JLabel(RLOTemp);
            rlo_temp_value.setFont(tp_font);
            JPanel rlo_panel = new JPanel(sizeLayout);
            rlo_panel.add(getPressureLabel());
            rlo_panel.add(rlo_pressure_value);
            rlo_panel.add(getTempLabel());
            rlo_panel.add(rlo_temp_value);

            panel12.add(rlo_panel);

            leftPanel.add(panel12);

            JPanel panel13 = new JPanel();
            panel13.setBorder(BorderFactory.createTitledBorder(null, "Rear Left Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

            JLabel rli_pressure_value = new JLabel("<html><font color='red'>" + RLIPressure + "</font></html>");
            rli_pressure_value.setFont(tp_font);
            JLabel rli_temp_value = new JLabel(RLITemp);
            rli_temp_value.setFont(tp_font);
            JPanel rli_panel = new JPanel(sizeLayout);
            rli_panel.add(getPressureLabel());
            rli_panel.add(rli_pressure_value);
            rli_panel.add(getTempLabel());
            rli_panel.add(rli_temp_value);

            panel13.add(rli_panel);

            leftPanel.add(panel13);

            leftPanel.setMaximumSize(leftPanel.getPreferredSize());
            leftPanel.setMinimumSize(leftPanel.getPreferredSize());

            // Center - bus image
            JPanel centralPanel = new JPanel();
            try {
                JLabel imgLabel = new JLabel();
                BufferedImage img = ImageIO.read(new File("bustyres.png"));
                Image bimg = img.getScaledInstance(250, 600, Image.SCALE_SMOOTH);
                ImageIcon imageIcon = new ImageIcon(bimg);
                imgLabel = new JLabel("", imageIcon, JLabel.CENTER);

                centralPanel.add(imgLabel);
            } catch (Exception e) {
                e.printStackTrace();
            }

            // Right side values
            JPanel rightPanel = new JPanel();
            BoxLayout rightLayout = new BoxLayout(rightPanel, BoxLayout.Y_AXIS);
            rightPanel.setLayout(rightLayout);

            JPanel panelFR = new JPanel();
            panelFR.setBorder(BorderFactory.createTitledBorder(null, "Front Right", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

            JLabel fr_pressure_value = new JLabel("<html><font color='red'>" + FRPressure + "</font></html>");
            fr_pressure_value.setFont(tp_font);

            JLabel fr_temp_value = new JLabel(FRTemp);
            fr_temp_value.setFont(tp_font);
            JPanel fr_panel = new JPanel(sizeLayout);
            fr_panel.add(getPressureLabel());
            fr_panel.add(fr_pressure_value);
            fr_panel.add(getTempLabel());
            fr_panel.add(fr_temp_value);

            panelFR.add(fr_panel);

            rightPanel.add(panelFR);

            JPanel panelRRO = new JPanel();
            panelRRO.setBorder(BorderFactory.createTitledBorder(null, "Rear Right Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

            JLabel rro_pressure_value = new JLabel("<html><font color='red'>" + RROPressure + "</font></html>");
            rro_pressure_value.setFont(tp_font);
            JLabel rro_temp_value = new JLabel(RROTemp);
            rro_temp_value.setFont(tp_font);
            JPanel rro_panel = new JPanel(sizeLayout);
            rro_panel.add(getPressureLabel());
            rro_panel.add(rro_pressure_value);
            rro_panel.add(getTempLabel());
            rro_panel.add(rro_temp_value);

            panelRRO.add(rro_panel);

            rightPanel.add(panelRRO);

            JPanel panelRRI = new JPanel();
            panelRRI.setBorder(BorderFactory.createTitledBorder(null, "Rear Right Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

            JLabel rri_pressure_value = new JLabel("<html><font color='red'>" + RRIPressure + "</font></html>");
            rri_pressure_value.setFont(tp_font);
            JLabel rri_temp_value = new JLabel(RRITemp);
            rri_temp_value.setFont(tp_font);
            JPanel rri_panel = new JPanel(sizeLayout);
            rri_panel.add(getPressureLabel());
            rri_panel.add(rri_pressure_value);
            rri_panel.add(getTempLabel());
            rri_panel.add(rri_temp_value);

            panelRRI.add(rri_panel);

            rightPanel.add(panelRRI);

            bottomMainPanel.add(leftPanel);
            bottomMainPanel.add(centralPanel);
            bottomMainPanel.add(rightPanel);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return bottomMainPanel;
    }

    private Connection connectToSQLite() {
        Connection conn = null;
        try {
            // db parameters
            Class.forName("org.sqlite.JDBC");
            String url = "jdbc:sqlite:/opt/JavaServices/sqlite/TPMS.db";
            // create a connection to the database
            conn = DriverManager.getConnection(url);
            System.out.println("Connection to SQLite has been established.");
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println(e.getMessage());
        }
        return conn;
    }
}

class Dummy {
    // just to have another thing to pack in the jar
}
