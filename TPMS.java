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
import java.util.Date;
import javax.swing.border.TitledBorder;

// follow the below link
//https://stackoverflow.com/questions/804466/how-do-i-create-executable-java-program
public class TPMS extends JFrame {

    PythonInterpreter interpreter = null;

    JPanel mainPanel = new JPanel();
    JPanel liveDataPanel = new JPanel();
    JPanel headerPanel = new JPanel(new GridLayout(1, 2));

    JLabel vehName_label_s = new JLabel();
    Font tp_font = new Font("Arial", Font.PLAIN, 30);
    Font tpHeader_font = new Font("Arial", Font.PLAIN, 15).deriveFont(Font.BOLD);

    JLabel fl_pressure_label_s = new JLabel(" --- ");
    JLabel fl_temp_label_s = new JLabel(" --- ");
    JLabel fr_pressure_label_s = new JLabel(" --- ");
    JLabel fr_temp_label_s = new JLabel(" --- ");
    JLabel rlo_pressure_label_s = new JLabel(" --- ");
    JLabel rlo_temp_label_s = new JLabel(" --- ");
    JLabel rli_pressure_label_s = new JLabel(" --- ");
    JLabel rli_temp_label_s = new JLabel(" --- ");
    JLabel rri_pressure_label_s = new JLabel(" --- ");
    JLabel rri_temp_label_s = new JLabel(" --- ");
    JLabel rro_pressure_label_s = new JLabel(" --- ");
    JLabel rro_temp_label_s = new JLabel(" --- ");

    // For Header
    JTextField searchBox = new JTextField();
    JButton bscan = new JButton("Scan");
    JButton bdone = new JButton("Done");

    // For keyboard
    JPanel keyboardPanel = new JPanel(new GridLayout(4, 3));
    JButton b1 = new JButton("1");
    JButton b2 = new JButton("2");
    JButton b3 = new JButton("3");
    JButton b4 = new JButton("4");
    JButton b5 = new JButton("5");
    JButton b6 = new JButton("6");
    JButton b7 = new JButton("7");
    JButton b8 = new JButton("8");
    JButton b9 = new JButton("9");
    JButton bbackspace = new JButton("Backspace");
    JButton b0 = new JButton("0");
    JButton bclear = new JButton("Clear");

    String numberString = "";
    long vehId = 0;
    String rfuid = null;

    public static void main(String[] args) {
        //Create and set up the window.
        TPMS tpms = new TPMS();
        tpms.initUI();
    }

    public void initUI() {

        setBackground(Color.BLACK);
        setTitle("Tyre Pressure & Temperature");

        // Create Search tab
        mainPanel.setLayout(new BorderLayout());

        // Design keyboard panel
        desingKeyboardPanel();

        desingStaticSearchTPScreen();

        headerPanel.setBorder(BorderFactory.createLineBorder(Color.black));

        searchBox.setHorizontalAlignment(SwingConstants.CENTER);
        searchBox.setPreferredSize(new Dimension(200, 80));
        searchBox.setFont(new Font("Arial", Font.PLAIN, 50));
        searchBox.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                System.out.println("text box selected - show keyboard");
                keyboardPanel.setVisible(true);
            }
        });

        bscan.setFont(new Font("Arial", Font.PLAIN, 40));
        bscan.setBackground(Color.GREEN);
        bscan.setForeground(Color.WHITE);

        bscan.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ae) {
                System.out.println("Scan selected - hide keyboard");
                findTPData();
            }
        });

        bdone.setFont(new Font("Arial", Font.PLAIN, 40));
        bdone.setBackground(Color.RED);
        bdone.setForeground(Color.WHITE);

        bdone.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ae) {
                System.out.println("done selected - hide keyboard");
                numberString = "";
                searchBox.setText("");
                // Remove Scan & add Done button
                searchBox.setVisible(true);
                headerPanel.add(searchBox);
                vehName_label_s.setVisible(false);
                headerPanel.remove(vehName_label_s);

                bscan.setVisible(true);
                headerPanel.add(bscan);
                bdone.setVisible(false);
                headerPanel.remove(bdone);

                try {
                    liveDataPanel.setVisible(false);
//                    mainPanel.remove(liveDataPanel);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                // add keyboard panel and remove live data Panel
                try {
                    keyboardPanel.setVisible(false);
//                    mainPanel.add(keyboardPanel, BorderLayout.CENTER);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        headerPanel.add(searchBox);
        headerPanel.add(bscan);

        mainPanel.add(headerPanel, BorderLayout.NORTH);

        // Add keyboard panel and dont visible it
        keyboardPanel.setVisible(false);
        JPanel borderCenterLayout = new JPanel();
        borderCenterLayout.add(keyboardPanel);

        liveDataPanel.setVisible(false);
        borderCenterLayout.add(liveDataPanel);

        mainPanel.add(borderCenterLayout, BorderLayout.CENTER);

        // Add live Temp & Pressure panel and dont show by default
//        liveDataPanel.setVisible(false);
//        mainPanel.add(liveDataPanel, BorderLayout.CENTER);
        // Add the tabs to screen
        getContentPane().add(mainPanel);

        // Adding to JFrame
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setExtendedState(JFrame.MAXIMIZED_BOTH);
        setUndecorated(true);
        setVisible(true);
        pack();
    }

    private void hideAndShowScreenItems_scan() {
        try {
            // Remove Scan & add Done button
            searchBox.setVisible(false);
            headerPanel.remove(searchBox);
            vehName_label_s.setVisible(true);
            headerPanel.add(vehName_label_s);
            bscan.setVisible(false);
            headerPanel.remove(bscan);
            bdone.setVisible(true);
            headerPanel.add(bdone);
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            // Remove keyboard panel and add live data Panel
            keyboardPanel.setVisible(false);
//                    mainPanel.remove(keyboardPanel);
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            liveDataPanel.setVisible(true);
//                    mainPanel.add(liveDataPanel, BorderLayout.CENTER);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void findTPData() {
        vehId = 0;
        rfuid = "";
        System.out.println("createSearchScreen " + searchBox.getText());
        if (null != searchBox.getText() && searchBox.getText().trim().length() >= 4) {
            Connection conn = connectToSQLite();
            try {
                Statement stmt = conn.createStatement();
                String sql = "SELECT * FROM DeviceDetails where vehName like '%" + searchBox.getText() + "%'";
                ResultSet rs = stmt.executeQuery(sql);
                if (rs.next()) {
                    rfuid = rs.getString("RFUID");
                    String btuid = rs.getString("BUID");
                    if (null != rfuid && rfuid.trim().length() > 0 && null != btuid && btuid.trim().length() > 0) {
                        JOptionPane.showMessageDialog(mainPanel, "Body message " + rfuid, "Warning", JOptionPane.PLAIN_MESSAGE);
                        vehId = rs.getLong("vehId");
                        updateTheTPLiveData();
                    }
                } else {
                    System.out.println("Vehicle not found with " + searchBox.getText());
                    JOptionPane.showMessageDialog(mainPanel, "Vehicle not found", "Warning", JOptionPane.PLAIN_MESSAGE);
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
            updateTheTPLiveData();
        }

    }

    public void updateTheTPLiveData() {
        System.out.println("start.TPMS.updateTheTPLiveData() " + vehId + " " + rfuid);
        try {
            // Call the python program
            TPMS ie = new TPMS();
//            ie.execfile("Python/blecontroller.py");
//            ie.execfile("Python/hello.py");
            ie.execfile("Python/work.py");
            String result = ie.getTPMSDetials(rfuid);
            if (null != result) {
                JOptionPane.showMessageDialog(mainPanel, result, "Warning", JOptionPane.PLAIN_MESSAGE);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("start.TPMS.updateTheTPLiveData() " + vehId + " " + new Date());
        Connection conn = connectToSQLite();
        try {
            Statement stmt = conn.createStatement();
            long local_vehId = 0;
            if (vehId != 0) {
                // Search vehicle data only
                local_vehId = vehId;
            } else {
                // Automatic data (Latest)
                String sql = "SELECT vehId FROM Latest_data where count <= 5 order by device_date_time DESC limit 1;";
                ResultSet rs = stmt.executeQuery(sql);
                if (rs.next()) {
                    local_vehId = rs.getLong("vehId");
                }
            }
            System.out.println("veh id " + local_vehId);
            String sql = "SELECT * FROM Latest_data where vehId = " + local_vehId;
            ResultSet rs1 = stmt.executeQuery(sql);
            System.out.println("start.TPMS.updateTheTPLiveData() "+rs1.getFetchSize());
//            if (rs1.getFetchSize() > 0) {
                hideAndShowScreenItems_scan();

                while (rs1.next()) {
                    try {
                        if (rs1.getString("location").equalsIgnoreCase("01")
                                || rs1.getString("location").equalsIgnoreCase("FL")) {
                            fl_pressure_label_s.setText(rs1.getString("pressure"));
                            fl_temp_label_s.setText(rs1.getString("temp"));
                        } else if (rs1.getString("location").equalsIgnoreCase("02")
                                || rs1.getString("location").equalsIgnoreCase("FR")) {
                            fr_pressure_label_s.setText(rs1.getString("pressure"));
                            fr_temp_label_s.setText(rs1.getString("temp"));
                        } else if (rs1.getString("location").equalsIgnoreCase("03")
                                || rs1.getString("location").equalsIgnoreCase("RLO")) {
                            rlo_pressure_label_s.setText(rs1.getString("pressure"));
                            rlo_temp_label_s.setText(rs1.getString("temp"));
                        } else if (rs1.getString("location").equalsIgnoreCase("04")
                                || rs1.getString("location").equalsIgnoreCase("RLI")) {
                            rli_pressure_label_s.setText(rs1.getString("pressure"));
                            rli_temp_label_s.setText(rs1.getString("temp"));
                        } else if (rs1.getString("location").equalsIgnoreCase("05")
                                || rs1.getString("location").equalsIgnoreCase("RRI")) {
                            rri_pressure_label_s.setText(rs1.getString("pressure"));
                            rri_temp_label_s.setText(rs1.getString("temp"));
                        } else if (rs1.getString("location").equalsIgnoreCase("06")
                                || rs1.getString("location").equalsIgnoreCase("RRO")) {
                            rro_pressure_label_s.setText(rs1.getString("pressure"));
                            rro_temp_label_s.setText(rs1.getString("temp"));
                        }
                    } catch (Exception ex) {
                        ex.printStackTrace();
                    }
                }
                sql = "SELECT vehName FROM DeviceDetails where vehId = " + local_vehId;
                ResultSet rs = stmt.executeQuery(sql);
                if (rs.next()) {
                    System.out.println("veh Name: " + rs.getString("vehName"));
                    vehName_label_s.setText(rs.getString("vehName"));
                }
//            } else {
//
//            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (conn != null) {
                    conn.close();
                    System.out.println("Connection closed");
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public void desingStaticSearchTPScreen() {
//        JPanel liveDataPanel = new JPanel();
        liveDataPanel.setLayout(new BorderLayout());
        try {
            vehName_label_s.setPreferredSize(
                    new Dimension(200, 70));
            vehName_label_s.setHorizontalAlignment(SwingConstants.CENTER);

            vehName_label_s.setFont(
                    new Font("Arial", Font.PLAIN, 40));
            liveDataPanel.add(vehName_label_s, BorderLayout.NORTH);

            JPanel bottomMainPanel = new JPanel(new GridLayout(1, 3));

            // For gaps between Temp & Pressure
            GridLayout sizeLayout = new GridLayout(2, 2, 10, 10);

            liveDataPanel.add(bottomMainPanel, BorderLayout.CENTER);
            try {
                // Left side values
                JPanel leftPanel = new JPanel();
                BoxLayout leftLayout = new BoxLayout(leftPanel, BoxLayout.Y_AXIS);
                leftPanel.setLayout(leftLayout);

                JPanel panel11 = new JPanel();
                panel11.setBorder(BorderFactory.createTitledBorder(null, "Front Left", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                fl_pressure_label_s.setFont(tp_font);
                fl_temp_label_s.setFont(tp_font);
                JPanel fl_panel = new JPanel(sizeLayout);
                fl_panel.add(getPressureLabel());
                fl_panel.add(fl_pressure_label_s);
                fl_panel.add(getTempLabel());
                fl_panel.add(fl_temp_label_s);

                panel11.add(fl_panel);

                leftPanel.add(panel11);

                JPanel panel12 = new JPanel();
                panel12.setBorder(BorderFactory.createTitledBorder(null, "Rear Left Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rlo_pressure_label_s.setFont(tp_font);
                rlo_temp_label_s.setFont(tp_font);
                JPanel rlo_panel = new JPanel(sizeLayout);
                rlo_panel.add(getPressureLabel());
                rlo_panel.add(rlo_pressure_label_s);
                rlo_panel.add(getTempLabel());
                rlo_panel.add(rlo_temp_label_s);

                panel12.add(rlo_panel);

                leftPanel.add(panel12);

                JPanel panel13 = new JPanel();
                panel13.setBorder(BorderFactory.createTitledBorder(null, "Rear Left Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rli_pressure_label_s.setFont(tp_font);
                rli_temp_label_s.setFont(tp_font);
                JPanel rli_panel = new JPanel(sizeLayout);
                rli_panel.add(getPressureLabel());
                rli_panel.add(rli_pressure_label_s);
                rli_panel.add(getTempLabel());
                rli_panel.add(rli_temp_label_s);

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

                fr_pressure_label_s.setFont(tp_font);
                fr_temp_label_s.setFont(tp_font);
                JPanel fr_panel = new JPanel(sizeLayout);
                fr_panel.add(getPressureLabel());
                fr_panel.add(fr_pressure_label_s);
                fr_panel.add(getTempLabel());
                fr_panel.add(fr_temp_label_s);

                panelFR.add(fr_panel);

                rightPanel.add(panelFR);

                JPanel panelRRO = new JPanel();
                panelRRO.setBorder(BorderFactory.createTitledBorder(null, "Rear Right Outer", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rro_pressure_label_s.setFont(tp_font);
                rro_temp_label_s.setFont(tp_font);
                JPanel rro_panel = new JPanel(sizeLayout);
                rro_panel.add(getPressureLabel());
                rro_panel.add(rro_pressure_label_s);
                rro_panel.add(getTempLabel());
                rro_panel.add(rro_temp_label_s);

                panelRRO.add(rro_panel);

                rightPanel.add(panelRRO);

                JPanel panelRRI = new JPanel();
                panelRRI.setBorder(BorderFactory.createTitledBorder(null, "Rear Right Inner", TitledBorder.LEFT, TitledBorder.TOP, tpHeader_font));

                rri_pressure_label_s.setFont(tp_font);
                rri_temp_label_s.setFont(tp_font);
                JPanel rri_panel = new JPanel(sizeLayout);
                rri_panel.add(getPressureLabel());
                rri_panel.add(rri_pressure_label_s);
                rri_panel.add(getTempLabel());
                rri_panel.add(rri_temp_label_s);

                panelRRI.add(rri_panel);

                rightPanel.add(panelRRI);

                bottomMainPanel.add(leftPanel);
                bottomMainPanel.add(centralPanel);
                bottomMainPanel.add(rightPanel);
            } catch (Exception e) {
                e.printStackTrace();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void desingKeyboardPanel() {
        try {
            System.out.println("start.TPMS.desingKeyboardPanel() " + new Date());

            // Create key board
            b1.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b1);
            b2.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b2);
            b3.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b3);
            b4.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b4);
            b5.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b5);
            b6.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b6);
            b7.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b7);
            b8.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b8);
            b9.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b9);
            bbackspace.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(bbackspace);
            b0.setFont(new Font("Arial", Font.PLAIN, 50));
            keyboardPanel.add(b0);
            bclear.setFont(new Font("Arial", Font.PLAIN, 40));
            keyboardPanel.add(bclear);

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
            bbackspace.addActionListener(listener);
            b9.addActionListener(listener);
            bclear.addActionListener(listener);

        } catch (Exception e) {
            e.printStackTrace();

        }
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
            } else if (e.getSource() == bbackspace) {
                if (numberString != null && numberString.length() > 0) {
                    numberString = numberString.substring(0, numberString.length() - 1);
                }
            }
            searchBox.setText(numberString);
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

    public TPMS() {
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

}
