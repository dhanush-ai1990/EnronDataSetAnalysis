/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package babel;

import it.uniroma1.lcl.jlt.util.Language;
import it.uniroma1.lcl.jlt.util.ScoredItem;
import it.uniroma1.lcl.jlt.util.Strings;
import it.uniroma1.lcl.jlt.ling.Word;
//import it.uniroma1.lcl.knowledge.*;
import it.uniroma1.lcl.babelnet.*;
//import it.uniroma1.lcl.knowledge.graph.*;
import java.io.IOException;
import java.util.*;
import it.uniroma1.lcl.babelnet.data.*;

/**
 *
 * @author Dhanush
 */
public class Babel {

	public static void main(String[] args) {

	BabelNet bn = BabelNet.getInstance();
        try{
        //List<BabelSynset> byl = bn.getSynsets("Pycharm", Language.EN,BabelPOS.NOUN,BabelSenseSource.WIKI);
        //System.out.println(byl);
        // Get the SyncSet Id eg : bn:02613259n for Pycharm
        for (BabelSynset synset : bn.getSynsets("Javascript", Language.EN)) {
            System.out.println("Synset ID: " + synset.getId());
        }
        }
          catch (IOException ioe)
                  {
                      System.out.println("Trouble: " + ioe.getMessage());
        }

}
}
    

